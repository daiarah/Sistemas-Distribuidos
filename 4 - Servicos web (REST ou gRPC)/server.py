# Avaliacao 4 (Leilao) - Sistemas Distribuidos 2023_1_S73
# Membros
# # Daiarah Kalil RA: 1774220
# # Lucas de Lima RA: 1774271

import time
import threading

from flask_sse import sse
from flask import Flask, request, jsonify

def resposta(code, msg = "Erro Interno"):
    response = jsonify(msg)
    response.headers["Content-Type"] = "application/json; charset=utf-8"
    response.status_code = code
    return response

class Cliente:
    def __init__(self, nome, cliente_topic):
        self.nome = nome
        self.cliente_topic = cliente_topic

class Servidor:
    def __init__(self):
        self.leiloes = {}
        self.clientes = {}

    def cadastrar_cliente(self, nome, cliente_topic):
        cliente_topic_str = str(cliente_topic)
        self.clientes[cliente_topic_str] = Cliente(nome, cliente_topic_str)
        msg = f"Cadastro finalizado para o cliente: {str(nome)}"
        return resposta(201, msg)

    def consultar_leiloes_ativos(self):
        try:
            # if not len(self.leiloes):
            #     raise SystemError
            existeLeilaoAtivo = False
            msg = f"\t\tLeilões ativos\n"

            for item in self.leiloes:
                leilao = self.leiloes[item]
                if leilao.tempo_atual > 0:
                    existeLeilaoAtivo = True
                    msg += f"Cod={leilao.cod_produto},Nome={leilao.nome},Descricao={leilao.descricao},Preco={leilao.preco_atual},TempoRestante={leilao.tempo_atual}\n"

            if not existeLeilaoAtivo:
                raise SystemError
            
            return resposta(200, msg)
        except SystemError:
            return resposta(400, "Nenhum leilão ativo no momento.\n")
        except Exception as ex:
            return resposta(500, str(ex))
            
    def cadastrar_produto(self, cliente_topic, codigo, nome, descricao, preco_inicial, tempo_final):
        self.leiloes[codigo] = Leilao(cliente_topic, codigo, nome, descricao, preco_inicial, tempo_final)
        # Notificar clientes sobre novo produto cadastrado em Leilão
        msg = f"Novo produto cadastrado, Cod = {codigo}, Nome = {nome}, Descricao = {descricao}, " + f" Preco Inicial = {preco_inicial}"
        # Notifica todos os clientes pelo canal padrão "sse"
        notificar_cliente(msg)

        return resposta(204, "")
        
    def dar_lance(self, cliente_topic, cod_produto, lance):
        msg = ""
        try:
            cliente = self.clientes[cliente_topic]

            if not cod_produto in self.leiloes:
                msg = f"Produto não cadastrado\n"
                raise ValueError(msg)
            
            leilao = self.leiloes[cod_produto]
            return leilao.dar_lance(cliente, cod_produto, lance)
        
        except ValueError as ex:
            raise ex

# Leilao nao tera informacao de todos os clientes do servidor
class Leilao:
    def __init__(self, cliente, cod_produto, nome, descricao, preco_inicial, tempo_final):
        self.cod_produto = cod_produto
        self.nome = nome
        self.descricao = descricao
        self.preco_atual = float(preco_inicial) if preco_inicial != '' else 0
        self.tempo_atual = float(tempo_final) if tempo_final != '' else 0
        self.vencedor = None
        self.frequencia_notificacao = 5
        self.interessados = {}
        self.registrar_interessado(cliente)

        t = threading.Thread(target=self.inicia_leilao)
        t.start()

    def inicia_leilao(self):
        while(1):
            try:
                with app.app_context():
                    self.atualiza_leilao()
                    
                time.sleep(self.frequencia_notificacao)
            except Exception as ex:
                return str(ex)

    def atualiza_leilao(self):
        self.tempo_atual -= self.frequencia_notificacao
        if self.tempo_atual <= 0:
            msg = f"O leilão do produto Cod {self.cod_produto} acabou!"

            if(self.vencedor):
                msg += f" Vencedor {self.vencedor.nome}, valor negociado {self.preco_atual}"
            else:
                msg += " Não houve vencedores."

            self.finalizar(msg)
            
    def notificar_interessados(self, msg):
        for interessado in self.interessados:
            notificar_cliente(msg, str(interessado))

    # Verificar se leilao ta ativo, se o valor é maior que o valor anterior
    def dar_lance(self, cliente, cod_produto, lance):
        valor = float(lance) if lance != '' else 0
        msg = ""
        try:
            if self.tempo_atual < 0:
                msg = f"Leilao encerrado\n"
                raise ValueError(msg)

            if valor <= self.preco_atual:
                msg = f"O lance de {valor} para o produto com código {cod_produto} deve ser maior que o valor atual de {self.preco_atual}"
                raise ValueError(msg)

            self.preco_atual = valor
            self.registrar_interessado(cliente.cliente_topic)
            msg = f"Novo lance para o produto {cod_produto}! Novo preço: {lance}"
            self.vencedor = cliente

            if len(self.interessados):
                # Notificar compradores interessados no produto
                self.notificar_interessados(msg)
            else:
                msg = ""

            return resposta(204, "")
        
        except ValueError as ex:
            raise ex

    def registrar_interessado(self, cliente_topic):
        self.interessados[cliente_topic] = cliente_topic

    def finalizar(self, msg):
        # with app.app_context():
        self.notificar_interessados(msg)
        self.interessados.clear()

servidor = Servidor()

def notificar_cliente(msg, cliente="sse"):
    sse.publish(msg, channel=cliente)

app = Flask(__name__)
app.config["REDIS_URL"] = "redis://localhost"
app.register_blueprint(sse, url_prefix='/stream')

@app.route('/cliente', methods=['POST'])
def cadastrar_cliente():
    try:
        data = request.get_json()
        nome = data['nome']
        cliente_topic = data['cliente_topic']
        return servidor.cadastrar_cliente(nome, cliente_topic)
    except KeyError as ex:
        return resposta(500, f"Erro na chave: {ex}")
    except Exception as ex:
        return resposta(500, str(ex))


@app.route('/leiloes', methods=['GET'])
def consultar_leiloes_ativos():
    try:
        return servidor.consultar_leiloes_ativos()
    except Exception as ex:
        return resposta(500, str(ex))

@app.route('/produto', methods=['POST'])
def cadastrar_produto():
    try:
        data = request.get_json()
        cliente_topic = data['cliente_topic']
        codigo = data['codigo']
        nome = data['nome']
        descricao = data['descricao']
        preco_inicial = data['preco_inicial']
        tempo_final = data['tempo_final']
        return servidor.cadastrar_produto(cliente_topic, codigo, nome, descricao, preco_inicial, tempo_final)

    except KeyError as ex:
        return resposta(500, f"Erro na chave: {ex}")
    except Exception as ex:
        return resposta(500, str(ex))

@app.route('/lance', methods=['POST'])
def dar_lance():
    try:
        data = request.get_json()
        cliente_topic = data['cliente_topic']
        cod_produto = data['cod_produto']
        lance = data['lance']
        return servidor.dar_lance(cliente_topic, cod_produto, lance)
    except KeyError as ex:
        return resposta(500, f"Erro na chave: {ex}")
    except ValueError as ex:
        return resposta(400, str(ex))
    except Exception as ex:
        return resposta(500, str(ex))
 
if __name__ == "__main__":
    # app.run()
    app.run(debug=True, threaded=True)

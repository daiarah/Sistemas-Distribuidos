# Avaliacao 3 (Leilao) - Sistemas Distribuidos 2023_1_S73
# Membros
# # Daiarah Kalil RA: 1774220
# # Lucas de Lima RA: 1774271

import Pyro5.api
import time
import Pyro5.api
import Pyro4
import threading
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.serialization import load_pem_public_key
import base64

pyroName = "PYRO:obj"

def uri_has_pyro(uri):
    return uri.lower().find(pyroName.lower()) != -1

def descryptography(value):
    return base64.b64decode(value['data'])

def notificar_cliente(cliente, msg):
    try:
        clienteProxy = None
        clienteStr = str(cliente)
        if uri_has_pyro(clienteStr):
            clienteProxy = Pyro5.api.Proxy(clienteStr)
        else:
            clienteProxy = Pyro5.api.Proxy(cliente.uri_cliente)

        clienteProxy.notificacao(msg)
        return True
    except:
        return True

class Cliente:
    def __init__(self, nome, uri_cliente, chave_publica):
        self.nome = nome
        self.uri_cliente = uri_cliente
        self.chave_publica = chave_publica

# Leilao nao tera informacao de todos os clientes do servidor
class Leilao:
    def __init__(self, cliente, cod_produto, nome, descricao, preco_inicial, tempo_final):
        self.cod_produto = cod_produto
        self.nome = nome
        self.descricao = descricao
        self.preco_atual = float(preco_inicial)
        self.tempo_atual = float(tempo_final)
        self.vencedor = None
        self.frequencia_notificacao = 5
        self.interessados = {}
        self.registrar_interessado(cliente)

        t = threading.Thread(target=self.inicia_leilao)
        t.start()

    def inicia_leilao(self):
        while(1):
            self.atualiza_leilao()
            time.sleep(self.frequencia_notificacao)

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
            notificar_cliente(str(interessado), msg)

    # Verificar se leilao ta ativo, se o valor é maior que o valor anterior
    def dar_lance(self, cliente, cod_produto, lance):
        valor = float(lance)
        msg = ""
        retorno = True
        try:
            if self.tempo_atual < 0:
                msg = f"Leilao encerrado\n"
                raise SystemError

            if valor <= self.preco_atual:
                msg = f"O lance de {valor} para o produto {cod_produto} menor que o valor atual {self.preco_atual}"
                raise SystemError

            self.preco_atual = valor
            self.registrar_interessado(cliente)
            msg = f"Novo lance para o produto {cod_produto}! Novo preço: {lance}"
            self.vencedor = cliente

        except:
            retorno = False
        finally:
            if len(self.interessados):
                # Notificar compradores interessados no produto
                self.notificar_interessados(msg)
            else:
                notificar_cliente(cliente, msg)
            # notificar_cliente(cliente, msg)
            return retorno

    def registrar_interessado(self, cliente):
        clienteStr = str(cliente)
        if uri_has_pyro(clienteStr):
            self.interessados[clienteStr] = cliente
        else:
            self.interessados[cliente.uri_cliente] = cliente.uri_cliente

    def finalizar(self, msg):
        self.notificar_interessados(msg)
        self.interessados.clear()

# configura uma instância única do servidor para ser consumida por diversos clientes
@Pyro4.behavior(instance_mode="single")
class Servidor:
    def __init__(self):
        self.leiloes = {}
        self.clientes = {}

    @Pyro5.api.expose
    def cadastrar_cliente(self, nome, uri_cliente, pem_public_key):
        # cliente = Pyro5.api.Proxy(uri_cliente)
        # Deserialize the PEM-encoded public key
        try:
            pem_bytes = descryptography(pem_public_key)
            public_key = serialization.load_pem_public_key(
                pem_bytes,
            )
            uri_cliente_str = str(uri_cliente)
            self.clientes[uri_cliente_str] = Cliente(nome, uri_cliente_str, public_key)
            msg = f"Cadastro finalizado para o cliente: {str(nome)}"
            return msg
        except:
            return f"Erro ao cadastrar o cliente: {str(nome)}"
        # cliente.notificacao(f"Cadastro finalizado para o cliente: {str(nome)}")

    @Pyro5.api.expose
    def consultar_leiloes_ativos(self, uri_cliente):
        try:
            cliente = Pyro5.api.Proxy(uri_cliente)
            if not len(self.leiloes):
                raise SystemError
            
            msg = f"\t\tLeilões ativos\n"
            # cliente.notificacao(msg)

            for item in self.leiloes:
                leilao = self.leiloes[item]
                if leilao.tempo_atual > 0:
                    msg += f"Cod={leilao.cod_produto},Nome={leilao.nome},Descricao={leilao.descricao},Preco={leilao.preco_atual},TempoRestante={leilao.tempo_atual}\n"
                    # cliente.notificacao(msg)

            return msg
        except:
            return f"Nenhum leilão ativo no momento.\n"
            
    @Pyro5.api.expose
    def cadastrar_produto(self, uri_cliente, codigo, nome, descricao, preco_inicial, tempo_final):
        self.leiloes[codigo] = Leilao(uri_cliente, codigo, nome, descricao, preco_inicial, tempo_final)
        try:
            # Notificar clientes sobre novo produto cadastrado em Leilão
            for cliente in self.clientes:
                # uri_cliente_str = str(cliente.uri_cliente)
                msg = f"Novo produto cadastrado, Cod = {codigo}, Nome = {nome}, Descricao = {descricao}, " + f" Preco Inicial = {preco_inicial}"
                notificar_cliente(str(cliente), msg)

            return True
        except:
            msg = f"Erro ao cadastrar produto Cod = {codigo}"
            notificar_cliente(str(cliente), msg)
            return False
        
    @Pyro5.api.expose
    def dar_lance(self, uri_cliente, cod_produto, lance, signature):
        uri_cliente_str = str(uri_cliente)
        msg = ""
        try:
            cliente = self.clientes[uri_cliente_str]

            if not self.verificar_assinatura(cliente.chave_publica, lance, signature):
                msg = f"Assinatura Inválida\n"
                raise SystemError

            if not cod_produto in self.leiloes:
                msg = f"Produto não cadastrado\n"
                raise SystemError
            
            leilao = self.leiloes[cod_produto]
            leilao.dar_lance(cliente, cod_produto, lance)

            return True
        except:
            notificar_cliente(uri_cliente_str, msg)
            return False
        
    def verificar_assinatura(self, public_key, msg, signature):
        try:
            public_key.verify(
                descryptography(signature),
                str(msg).encode("utf-8"),
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA256()
            )
            return True
        except:
            return False
        
def main():
    # registra a aplicação do servidor no serviço de nomes
    Pyro5.nameserver.start_ns()
    daemon = Pyro5.server.Daemon()
    ns = Pyro5.api.locate_ns()

    # localServer = Servidor()
    uri = daemon.register(Servidor)
    ns.register("AplicacaoServidor", uri)

    print("A aplicação está ativa")
    daemon.requestLoop()

if __name__ == "__main__":
    main()

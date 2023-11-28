# Avaliacao 3 (Leilao) - Sistemas Distribuidos 2023_1_S73
# Membros
# # Daiarah Kalil RA: 1774220
# # Lucas de Lima RA: 1774271

import Pyro5.api
import threading
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.serialization import load_pem_public_key
import random
from datetime import datetime
from Telas import menuPrincipal

random.seed(datetime.now().timestamp())

# Generate a private key
private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048,
)

# Get the public key object corresponding to the private key
public_key = private_key.public_key()
 
@Pyro5.api.expose
@Pyro5.api.callback
class cliente_callback(object):
    def notificacao(self, msg):
        print(str(msg))

    def loopThread(daemon):
    # thread para ficar escutando chamadas de método do servidor
        daemon.requestLoop()

def main():
    # Obtém a referência da aplicação do servidor no serviço de nomes
    ns = Pyro5.api.locate_ns()
    uri = ns.lookup("AplicacaoServidor")
    servidor = Pyro5.api.Proxy(uri)
    # Inicializa o Pyro daemon e registra o objeto Pyro callback nele.
    daemon = Pyro5.server.Daemon()
    callback = cliente_callback()
    uri_cliente = daemon.register(callback)

    # Inicializa a thread para receber notificações do servidor
    thread = threading.Thread(target=cliente_callback.loopThread, args=(daemon, ))
    thread.daemon = True
    thread.start()

    # Invoca método no servidor, passando a referência
    print("Cadastrando o cliente: \n", uri_cliente)

    pem_public_key = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo)

    print("Insira o nome do cliente: ")
    nome = input()
    print(servidor.cadastrar_cliente(nome, uri_cliente, pem_public_key))

    menuPrincipal.chamaMenu(servidor, uri_cliente, private_key)

if __name__ == "__main__":
    main()

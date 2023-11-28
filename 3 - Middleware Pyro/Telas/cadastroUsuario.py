
import tkinter as tk

class CadastroUsuario:
    def __init__(self, janela_usuario, servidor, uri_cliente, pem_public_key):
        self.janela_usuario = janela_usuario
        self.janela_usuario.title("Leilão - Cadastro de Cliente")
        self.janela_usuario.geometry("200x150")

        # Labels
        self.label_nome = tk.Label(self.janela_usuario, text="Nome:")
        self.label_nome.grid(row=0, column=0, padx=5, pady=5)

        # Entradas
        self.input_nome = tk.Entry(self.janela_usuario)
        self.input_nome.grid(row=0, column=1, padx=5, pady=5)

        # Botao
        self.botao_cadastrar = tk.Button(self.janela_usuario, text="Cadastrar", command= lambda: self.cadastrar(servidor, uri_cliente, pem_public_key))
        self.botao_cadastrar.grid(row=3, column=1, padx=5, pady=5)

    def cadastrar(self, servidor, uri_cliente, pem_public_key):
        nome = self.input_nome.get()

        servidor.cadastrar_cliente(nome, uri_cliente, pem_public_key)
        # Limpa as entradas após o cadastro
        self.input_nome.delete(0, tk.END)

def createCadastroUsuario(servidor, uri_cliente, pem_public_key):
    root = tk.Tk()
    root.iconbitmap('Telas\leilao.ico')
    tela = CadastroUsuario(root, servidor, uri_cliente, pem_public_key)
    root.mainloop()

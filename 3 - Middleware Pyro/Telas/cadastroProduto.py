
import tkinter as tk

class CadastroProduto:
    def __init__(self, janela_produto, servidor, uri_cliente):
        self.janela_produto = janela_produto
        self.janela_produto.title("Leilão - Cadastro de Produto")
        self.janela_produto.geometry("320x250")

        # Labels
        self.label_codigo = tk.Label(self.janela_produto, text="Código:")
        self.label_codigo.grid(row=0, column=0, padx=5, pady=5)

        self.label_nome = tk.Label(self.janela_produto, text="Nome:")
        self.label_nome.grid(row=1, column=0, padx=5, pady=5)

        self.label_descricao = tk.Label(self.janela_produto, text="Descrição:")
        self.label_descricao.grid(row=2, column=0, padx=5, pady=5)

        self.label_preco_inicial = tk.Label(self.janela_produto, text="Preço Inicial:")
        self.label_preco_inicial.grid(row=3, column=0, padx=5, pady=5)

        self.label_tempo_final = tk.Label(self.janela_produto, text="Tempo Final em segundos:")
        self.label_tempo_final.grid(row=4, column=0, padx=5, pady=5)

        # Entradas
        self.input_codigo = tk.Entry(self.janela_produto)
        self.input_codigo.grid(row=0, column=1, padx=5, pady=5)

        self.input_nome = tk.Entry(self.janela_produto)
        self.input_nome.grid(row=1, column=1, padx=5, pady=5)

        self.input_descricao = tk.Entry(self.janela_produto)
        self.input_descricao.grid(row=2, column=1, padx=5, pady=5)

        self.input_preco_inicial = tk.Entry(self.janela_produto)
        self.input_preco_inicial.grid(row=3, column=1, padx=5, pady=5)

        self.input_tempo_final = tk.Entry(self.janela_produto)
        self.input_tempo_final.grid(row=4, column=1, padx=5, pady=5)

        # Botao
        self.botao_cadastrar = tk.Button(self.janela_produto, text="Cadastrar", command=lambda: self.cadastrar(servidor, uri_cliente))
        self.botao_cadastrar.grid(row=5, column=1, padx=5, pady=5)

    def cadastrar(self, servidor, uri_cliente):
        codigo = self.input_codigo.get()
        nome = self.input_nome.get()
        descricao = self.input_descricao.get()
        preco_inicial = self.input_preco_inicial.get()
        tempo_final = self.input_tempo_final.get()

        if servidor.cadastrar_produto(uri_cliente, codigo, nome, descricao, preco_inicial, tempo_final):
            # Limpa as entradas após o cadastro
            self.input_codigo.delete(0, tk.END)
            self.input_nome.delete(0, tk.END)
            self.input_descricao.delete(0, tk.END)
            self.input_preco_inicial.delete(0, tk.END)
            self.input_tempo_final.delete(0, tk.END)

def createCadastroProduto(servidor, uri_cliente):
    root = tk.Tk()
    root.iconbitmap('Telas\leilao.ico')
    tela = CadastroProduto(root, servidor, uri_cliente)
    root.mainloop()   

if __name__ == '__main__':
    createCadastroProduto()


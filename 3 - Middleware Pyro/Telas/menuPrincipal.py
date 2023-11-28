import tkinter as tk
from Telas import cadastroProduto, consultaLeiloesAtivos, darLance, notificacoes

class MenuPrincipal:
    def __init__(self, janela_menu, servidor, uri_cliente, private_key):
        self.janela_menu = janela_menu
        self.janela_menu.title("Leilão - Menu Principal")
        self.janela_menu.geometry("300x200")

         # Botao
        self.botao_cadastro_produto = tk.Button(self.janela_menu, text="Cadastrar Produto", command=lambda: cadastroProduto.createCadastroProduto(servidor, uri_cliente))
        self.botao_cadastro_produto.grid(row=1, column=1, padx=5, pady=5)

        self.botao_consulta = tk.Button(self.janela_menu, text="Consultar Leilões Ativos", command=lambda: consultaLeiloesAtivos.createConsultaLeiloesAtivos(servidor, uri_cliente))
        self.botao_consulta.grid(row=2, column=1, padx=5, pady=5)

        self.botao_lance = tk.Button(self.janela_menu, text="Dar Lance", command=lambda: darLance.createDarLance(servidor, uri_cliente, private_key))
        self.botao_lance.grid(row=3, column=1, padx=5, pady=5)

def chamaMenu(servidor, uri_cliente, private_key):
    root = tk.Tk()
    root.iconbitmap('Telas\leilao.ico')
    app = MenuPrincipal(root, servidor, uri_cliente, private_key)
    root.mainloop()   

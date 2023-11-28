import sys
import tkinter as tk
import cadastroProduto, consultaLeiloesAtivos, darLance

class MenuPrincipal:
    def __init__(self, janela_menu, cliente_topic):
        self.janela_menu = janela_menu
        self.janela_menu.title("Leilão - Menu Principal")
        self.janela_menu.geometry("300x200")

        #  Botao
        self.botao_cadastro_produto = tk.Button(self.janela_menu, text="Cadastrar Produto", command= lambda: cadastroProduto.createCadastroProduto(cliente_topic))
        self.botao_cadastro_produto.grid(row=1, column=1, padx=5, pady=5)

        self.botao_consulta = tk.Button(self.janela_menu, text="Consultar Leilões Ativos", command=consultaLeiloesAtivos.createConsultaLeiloesAtivos)
        self.botao_consulta.grid(row=2, column=1, padx=5, pady=5)

        self.botao_lance = tk.Button(self.janela_menu, text="Dar Lance", command=lambda: darLance.createDarLance(cliente_topic))
        self.botao_lance.grid(row=3, column=1, padx=5, pady=5)

    # def dar_lance(self, cliente_topic):
        # print(darLance.createDarLance(cliente_topic))

def chamaMenu(cliente_topic):
    root = tk.Tk()
    root.iconbitmap('Telas\leilao.ico')
    app = MenuPrincipal(root, cliente_topic)
    root.mainloop()   

if __name__ == '__main__':
    if len(sys.argv) > 1:
        cliente_topic = sys.argv[1]
        chamaMenu(cliente_topic)
    else:
        print("Argumento ausente.")

import tkinter as tk

class ConsultaLeiloesAtivos:
    def __init__(self, janela_consulta):
        self.janela_consulta = janela_consulta
        self.janela_consulta.title("Leilão - Consulta Leilões Ativos")
        self.janela_consulta.geometry("350x150")
        self.janela_consulta.iconbitmap('Telas\leilao.ico')

def createConsultaLeiloesAtivos(servidor, uri_cliente):
    # root = tk.Tk()
    # tela = ConsultaLeiloesAtivos(root)
    # texto = tk.Text(root)
    # texto.pack()

    print(servidor.consultar_leiloes_ativos(uri_cliente))
    # with open("produtos.txt", "r") as arquivo:
    #     for linha in arquivo:
    #         texto.insert(tk.END, linha)    

    # root.mainloop()   

import tkinter as tk

class Notificacoes:
    def __init__(self, janela_consulta):
        self.janela_consulta = janela_consulta
        self.janela_consulta.title("Leilão - Consulta Leilões Ativos")
        self.janela_consulta.geometry("350x150")
        self.janela_consulta.iconbitmap('Telas\leilao.ico')

def createNotificacoes():
    root = tk.Tk()
    tela = Notificacoes(root)
    texto = tk.Text(root)
    texto.pack()
    with open("produtos.txt", "r") as arquivo:
        for linha in arquivo:
            texto.insert(tk.END, linha)    

    root.mainloop()   

if __name__ == '__main__':
    createNotificacoes()


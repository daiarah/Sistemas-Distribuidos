
import tkinter as tk
import requests

class DarLance:
    def __init__(self, janela_lance, cliente_topic):
        self.janela_lance = janela_lance
        self.janela_lance.title("Leilão - Dar Lance")
        self.janela_lance.geometry("320x150")

        # Labels
        self.label_id_produto = tk.Label(self.janela_lance, text="Cod do Produto:")
        self.label_id_produto.grid(row=0, column=0, padx=5, pady=5)

        self.label_valor = tk.Label(self.janela_lance, text="Valor:")
        self.label_valor.grid(row=1, column=0, padx=5, pady=5)

        # Entradas
        self.input_cod_produto = tk.Entry(self.janela_lance)
        self.input_cod_produto.grid(row=0, column=1, padx=5, pady=5)

        self.input_valor = tk.Entry(self.janela_lance)
        self.input_valor.grid(row=1, column=1, padx=5, pady=5)

        # Botao
        self.botao_dar_lance = tk.Button(self.janela_lance, text="Dar Lance", command=lambda: self.lance(cliente_topic))
        self.botao_dar_lance.grid(row=3, column=1, padx=5, pady=5)
    
    def lance(self, cliente_topic):
        cod_produto = self.input_cod_produto.get()
        valor = self.input_valor.get()

        url = "http://127.0.0.1:5000/lance"
        response = requests.post(url, json={'cliente_topic': cliente_topic, 'cod_produto': cod_produto, 'lance': valor})
        if isSuccessCode(response.status_code):
            # Limpa as entradas após o lance
            # response_json = response.json()
            # print(response_json)
            cod_produto = self.input_cod_produto.delete(0, tk.END)
            valor = self.input_valor.delete(0, tk.END)  
        else:
            response_json = response.json()
            print(response_json)

def isSuccessCode(code):
    return code >= 200 and code < 300

def createDarLance(cliente_topic):
    root = tk.Tk()
    root.iconbitmap('Telas\leilao.ico')
    tela = DarLance(root, cliente_topic)
    root.mainloop()   

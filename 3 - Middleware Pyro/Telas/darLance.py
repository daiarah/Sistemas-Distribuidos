
import tkinter as tk
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes

class DarLance:
    def __init__(self, janela_lance, servidor, uri_cliente, private_key):
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
        self.botao_dar_lance = tk.Button(self.janela_lance, text="Dar Lance", command=lambda: self.lance(servidor, uri_cliente, private_key))
        self.botao_dar_lance.grid(row=3, column=1, padx=5, pady=5)
    
    def lance(self, servidor, uri_cliente, private_key):
        cod_produto = self.input_cod_produto.get()
        valor = float(self.input_valor.get())

        signature = private_key.sign(
                        str(valor).encode("utf-8"),
                        padding.PSS(
                            mgf=padding.MGF1(hashes.SHA256()),
                            salt_length=padding.PSS.MAX_LENGTH
                    ),
                        hashes.SHA256()
                    )
        if servidor.dar_lance(uri_cliente, cod_produto, valor, signature):
            # Limpa as entradas após o lance
            cod_produto = self.input_cod_produto.delete(0, tk.END)
            valor = self.input_valor.delete(0, tk.END)    

def createDarLance(servidor, uri_cliente, private_key):
    root = tk.Tk()
    root.iconbitmap('Telas\leilao.ico')
    tela = DarLance(root, servidor, uri_cliente, private_key)
    root.mainloop()   

if __name__ == '__main__':
    createDarLance()


import tkinter as tk
import requests

class ConsultaLeiloesAtivos:
    def __init__(self, janela_consulta):
        self.janela_consulta = janela_consulta
        self.janela_consulta.title("Leilão - Consulta Leilões Ativos")
        self.janela_consulta.geometry("350x150")
        self.janela_consulta.iconbitmap('Telas\leilao.ico')

def createConsultaLeiloesAtivos():
    url = "http://127.0.0.1:5000/leiloes"
    response = requests.get(url)
    response_json = response.json()
    print(response_json)
    
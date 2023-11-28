# Producer 01
# Topicos: Saude e Financas

from confluent_kafka import Producer
import time
import random

config = {'bootstrap.servers':'localhost:9092'}
p = Producer(config)

print('Produtor 1 do Kafka foi inicializado...')
topic1 = "saude"
topic2 = "financas"

saude = ["Variante genética protege indígenas da Amazônia de doença de Chagas\n",
"Sedentarismo tem consequências graves; veja como manter uma vida ativa\n",
"Dor na perna? Saiba se ela pode ser provocada por um problema na coluna\n"]
financas = ["Poupança sobe, Bolsa desaba e vira pior aplicação no semestre\n",
"Rendimento médio de ETFs cai 14% no ano; é melhor investir em fundos agora?\n",
"Além da Eletrobras: Veja como investir em outras ações de energia elétrica\n"]

def main():
    while(1):

        p.produce(topic1, random.choice(saude).encode('utf-8'))
        p.flush()
        time.sleep(1)
        
        p.produce(topic2, random.choice(financas).encode('utf-8'))
        p.flush()
        time.sleep(3)
        
if __name__ == '__main__':
    main()
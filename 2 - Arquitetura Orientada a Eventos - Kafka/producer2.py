# Producer 02
# Topico: Esportes

from confluent_kafka import Producer
import time
import random

config = {'bootstrap.servers':'localhost:9092'}
p = Producer(config)

print('Produtor 2 do Kafka foi inicializado...')
topic3 = "esportes"

esportes = ["Após protesto, Wendie Renard volta à seleção francesa como capitã\n",
"F1 - \"Era uma vez a Ferrari\": Imprensa italiana diz que equipe \"afunda\" com problemas em 2023\n",
"\'Gabigol e Pedro não jogarem juntos é inadmissível\', afirma RMP\n"]

def main():
    while(1):

        p.produce(topic3, random.choice(esportes).encode('utf-8'))
        p.flush()
        time.sleep(3)
        
if __name__ == '__main__':
    main()
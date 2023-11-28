# Cosumidor 2: consome esportes (topico 3, producer 2)

from confluent_kafka import Consumer

config = {'bootstrap.servers':'localhost:9092','group.id':'consumer2','auto.offset.reset':'earliest'}
        
c = Consumer(config)
print('Tópicos disponíveis para consumo: ', c.list_topics().topics, "\n")

c.subscribe(['esportes'])

def main():
    while True:
        msg=c.poll(1.0) #timeout
        if msg is None:
            continue
        if msg.error():
            #print('Error: {}'.format(msg.error()))
            continue
        data=msg.value().decode('utf-8')
        print(data)
    c.close()
        
if __name__ == '__main__':
    main()
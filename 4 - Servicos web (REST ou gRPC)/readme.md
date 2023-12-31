Comandos antes de iniciar a aplicação:

docker-compose up -d

pip install -r requirements.txt

npm install

----------
INSTRUÇÕES:

Vamos continuar com a aplicação anterior. Porém, cliente e servidor precisam estar em linguagens de programação diferentes. O mais fácil é alterar a linguagem do cliente. Mas, vocês podem alterar a linguagem do cliente e do servidor, caso não queiram mais usar Python.

Não precisa mais assinar as mensagens de lance.

Para prover a comunicação entre os processos deve-se utilizar REST ou gRPC e não mais Pyro.

Para o envio das notificações de eventos, vocês vão utilizar o SSE (Server-Sent Events).

Resumindo:
- Duas linguagens de programação diferentes;
- Uso de REST ou gRPC para comunicação entre clientes e servidor;
- Uso do SSE para envio das notificações do servidor para os clientes.

Seguem alguns links para implementar o SSE (Server-Sent Events) usando diferentes linguagens:

https://www.baeldung.com/java-ee-jax-rs-sse
https://www.ibm.com/docs/pt-br/was-liberty/base?topic=liberty-starting-server-sent-events
https://www.velotio.com/engineering-blog/how-to-implement-server-sent-events-using-python-flask-and-react
https://sairamkrish.medium.com/handling-server-send-events-with-python-fastapi-e578f3929af1
*** Uso de canais: https://flask-sse.readthedocs.io/en/latest/advanced.html

https://github.com/tserkov/vue-sse
https://chrisblackwell.me/server-sent-events-using-laravel-vue/

https://www.woolha.com/tutorials/node-js-sse-server-sent-events-example-javascript-client

https://medium.com/@chrisbautistaaa/server-sent-events-in-angular-node-908830cc29aa

https://docs.servicestack.net/csharp-server-events-client
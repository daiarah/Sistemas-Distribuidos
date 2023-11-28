const { spawn } = require('child_process');
const EventSource = require('eventsource');
const { v4: uuidv4 } = require('uuid');
const readline = require('readline');

// Create readline interface
const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout,
});

const guid = uuidv4();
var cliente_topic = guid.substring(0, 8);

rl.question('Digite o nome do usuário: ', (nome) => {

  // Close the readline interface
  rl.close();

  // Cadastrar cliente no leilao
  var url = "http://127.0.0.1:5000/cliente";
  fetch(url,
    {
      method: 'POST',
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({"nome": nome, "cliente_topic": cliente_topic})
    })
    .then(response => response.json())
    .then(data => {
      console.log(data);
    })

  var channels = [cliente_topic, 'sse']; // Lista de canais que você deseja ouvir

  channels.forEach((channel) => {
    var url = `http://127.0.0.1:5000/stream?channel=${channel}`;
    const es = new EventSource(url);

    const listener = function (event) {
      var type = event.type;
      if (type != 'message')
      {
        console.log(`${type}: ${event.data || es.url}`);
      }
      else
      {
        console.log(event.data);
      }

      if (type === 'result') {
        es.close();
      }
    };

    es.addEventListener('message', listener);
    es.addEventListener('error', listener);
    es.addEventListener('result', listener);
  });

  spawn('python', ['Telas/menuPrincipal.py', cliente_topic], { stdio: 'inherit' });
});

var prefix = Deck.prefix
var transform = prefix('transform')
var translate = Deck.translate

var $container = document.getElementById('container')
var $topbar = document.getElementById('topbar')

var $poker = document.createElement('button')
var $play = document.createElement('button')
var $ready = document.createElement('button')

$ready.textContent = 'Ready'
$play.textContent = 'Play'

$topbar.appendChild($ready)
$topbar.appendChild($play)

var deck;

// create WebSocket connection
if (!window.WebSocket && window.MozWebSocket) {
  window.WebSocket = window.MozWebSocket;
}
var ws = new WebSocket('ws://192.168.0.110:8080/websocket');
var player_id;

ws.onopen = function(evt) {
  var msg ={};
  msg.action = "get"
  msg.data = ""
  msg = JSON.stringify(msg)
  ws.send(msg);
}

ws.onmessage = function(evt) {
  var data = JSON.parse(evt.data);
  if(data.type == "init") {
    deck = Deck(data.cards)
    player_id = data.player_id
    deck.mount($container)
  }
  else if (data.type == "ready") {
    console.log(data.start)
    if (data.start) {
      deck.cards.sort(function (a, b) {
        return a.rank - b.rank;
      });
      deck.poker()
    }
  }
  else if (data.type == "play") {
    console.log(data.playCards)
    if (data.playCards) {
      if (player_id == data.player_id) {
        deck.playPost()
      }
      deck.showCards(data)
    }
  }
}

$ready.addEventListener('click', function() {
  var msg = {}
  msg.action = "put"
  msg.data = ""
  msg = JSON.stringify(msg)
  ws.send(msg);
})

$play.addEventListener('click', function() {
  deck.play()
  var data = {}
  data.playCards = deck.playCards

  var msg = {}
  msg.action = "post"
  msg.data = data
  msg = JSON.stringify(msg);
  ws.send(msg);
})


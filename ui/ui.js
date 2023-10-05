var prefix = Deck.prefix
var transform = prefix('transform')
var translate = Deck.translate

var $container = document.getElementById('container')
var $topbar = document.getElementById('topbar')

var $poker = document.createElement('button')
var $play = document.createElement('button')

$poker.textContent = 'Poker'
$play.textContent = 'Play'

$topbar.appendChild($poker)
$topbar.appendChild($play)

var deck;

// create WebSocket connection
if (!window.WebSocket && window.MozWebSocket) {
  window.WebSocket = window.MozWebSocket;
}
var ws = new WebSocket('ws://127.0.0.1:8080/websocket');

ws.onopen = function(evt) {
  var msg ={};
  msg.action = "get"
  msg.data = "None"
  msg = JSON.stringify(msg)
  ws.send(msg);
}
ws.onmessage = function(evt) {
  var data = JSON.parse(evt.data);
  if(data.type == "poker"){
    deck =  Deck(data.cards)
    deck.pos = data.index
    deck.mount($container)
  }else if(data.type == "post"){
    console.log(data.postCards)
    if (data.postCards != "check_fail") {
      deck.prePost = data.postCards
      if (deck.pos == data.index) {
        deck.playPost()
      }
      deck.showCards(data)
    }
  }
}

$play.addEventListener('click', function() {
  deck.play()
  var data = {}
  data.cards = deck.post
  data.pre_post = deck.prePost

  var msg = {}
  msg.action = "post"
  msg.data = data
  msg = JSON.stringify(msg);
  ws.send(msg);
})
$poker.addEventListener('click', function () {
  deck.cards.sort(function (a, b) {
    return a.rank - b.rank;
  });
  deck.poker()
})


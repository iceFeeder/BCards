var prefix = Deck.prefix
var transform = prefix('transform')
var translate = Deck.translate

var $container = document.getElementById('container')
var $topbar = document.getElementById('topbar')

var $sort = document.createElement('button')
var $poker = document.createElement('button')
var $play = document.createElement('button')

$sort.textContent = 'Sort'
$poker.textContent = 'Poker'
$play.textContent = 'Play'

$topbar.appendChild($poker)
$topbar.appendChild($sort)
$topbar.appendChild($play)

var deck;
var sortType = 0;

// create WebSocket connection
if (!window.WebSocket && window.MozWebSocket) {
  window.WebSocket = window.MozWebSocket;
}
var ws = new WebSocket('ws://127.0.0.1:8080/websocket');
var MSG = '{"action":"ACTION","data":"DATA"}';

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
    deck.pre = data.data
    console.log(data.data)
  }
}

$sort.addEventListener('click', function () {
  deck.sort()
})
$play.addEventListener('click', function() {
  deck.play()
  var playCards = []
  deck.post.forEach(function (card){
    playCards.push(card.i)
  });

  var data = {}
  data.cards = playCards
  data.pre = deck.pre

  var msg = {}
  msg.action = "post"
  msg.data = data
  msg = JSON.stringify(msg);
  ws.send(msg);
})
$poker.addEventListener('click', function () {
  deck.queue(function (next) {
    deck.cards.forEach(function (card, i) {
      setTimeout(function () {
        card.setSide('back')
      }, i * 7.5)
    })
    next()
  })
  deck.sort(sortType)
  sortType ^= 1
  deck.poker()
})


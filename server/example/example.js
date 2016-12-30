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

var deck;
var sortType = 0;

// create WebSocket connection
if (!window.WebSocket && window.MozWebSocket) {
  window.WebSocket = window.MozWebSocket;
}
var ws = new WebSocket('ws://127.0.0.1:8080/websocket');
ws.onopen = function(evt) {
  ws.send('{"action":"'+"get"+'"'+"}");
}
ws.onmessage = function(evt) {
  var data = JSON.parse(evt.data);
  deck =  Deck(data.cards)
  deck.mount($container)
}

$sort.addEventListener('click', function () {
  deck.sort()
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


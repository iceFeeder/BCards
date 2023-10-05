var prefix = Deck.prefix
var transform = prefix('transform')
var translate = Deck.translate

var $container = document.getElementById('container')
var $topbar = document.getElementById('topbar')

var $ready = document.createElement('button')
var $play = document.createElement('button')
var $pass = document.createElement('button')

$ready.textContent = 'Ready'
$play.textContent = 'Play'
$pass.textContent = 'Pass'

$topbar.appendChild($ready)
$topbar.appendChild($play)
$topbar.appendChild($pass)

var deck;

// create WebSocket connection
if (!window.WebSocket && window.MozWebSocket) {
  window.WebSocket = window.MozWebSocket;
}
var ws = new WebSocket('ws://192.168.0.110:8080/websocket');
var player_id;
var cur_player_id;

ws.onopen = function(evt) {
  var msg ={};
  msg.action = "get_cards"
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
      cur_player_id = data.cur_player_id
      console.log("cur player id: " + cur_player_id)
    }
  }
  else if (data.type == "play") {
    console.log(data.playCards)
    if (data.playCards.length > 0) {
      cur_player_id = data.cur_player_id
      console.log("cur player id: " + cur_player_id)
      if (player_id == data.player_id) {
        deck.playPost()
      }
      deck.showCards(data)
    }
  }
  else if (data.type == "pass") {
    cur_player_id = data.cur_player_id
    console.log("cur player id: " + cur_player_id)
  }
}

$ready.addEventListener('click', function() {
  var msg = {}
  msg.action = "ready"
  msg.data = ""
  msg = JSON.stringify(msg)
  ws.send(msg);
})

$play.addEventListener('click', function() {
  if (cur_player_id != player_id) {
    console.log("not my turn...")
    return
  }
  deck.play()
  var data = {}
  data.playCards = deck.playCards

  var msg = {}
  msg.action = "post_cards"
  msg.data = data
  msg = JSON.stringify(msg);
  ws.send(msg);
})

$pass.addEventListener('click', function() {
  if (cur_player_id != player_id) {
    console.log("not my turn...")
    return
  }
  var msg = {}
  msg.action = "pass_turn"
  msg.data = ""
  msg = JSON.stringify(msg);
  ws.send(msg);
})


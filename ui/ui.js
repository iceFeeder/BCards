var prefix = Deck.prefix
var transform = prefix('transform')
var translate = Deck.translate

var $container = document.getElementById('container')
var $topbar = document.getElementById('topbar')
var $discard = document.getElementById('discard')
var $bottombar = document.getElementById('bottombar')

var $ready = document.createElement('button')
var $play = document.createElement('button')
var $pass = document.createElement('button')
var $playname = document.createElement('div')

$ready.textContent = 'Ready'
$play.textContent = 'Play'
$pass.textContent = 'Pass'
$play.right = 0

$topbar.appendChild($ready)
$bottombar.appendChild($playname)

var deck;
var discardCards;

// create WebSocket connection
if (!window.WebSocket && window.MozWebSocket) {
  window.WebSocket = window.MozWebSocket;
}
var ws = new WebSocket('ws://192.168.0.101:8080/websocket');
var player_id;
var cur_player_id;

function change_name_color() {
  if (cur_player_id == player_id) {
    $playname.style.color = '#33cd3c'
  } else {
    $playname.style.color = '#fff'
  }
}

ws.onopen = function(evt) {
}

ws.onmessage = function(evt) {
  var data = JSON.parse(evt.data);
  if (data.type == "ready") {
    console.log(data.start)
    if (data.start) {
      if (deck) {
        deck.unmount()
      }
      deck = Deck(data.cards)
      player_id = data.player_id
      $playname.textContent = "Player" + player_id
      deck.mount($container)
      deck.cards.sort(function (a, b) {
        return a.rank - b.rank;
      });
      deck.poker()
      cur_player_id = data.cur_player_id
      change_name_color()
      $topbar.removeChild($ready)
      $bottombar.appendChild($play)

      $topbar.appendChild($pass)
      console.log("cur player id: " + cur_player_id)
    }
  }
  else if (data.type == "play") {
    console.log(data.playCards)
    if (data.playCards.length > 0) {
      cur_player_id = data.cur_player_id
      console.log("cur player id: " + cur_player_id)
      change_name_color()
      if (player_id == data.player_id) {
        deck.playPost()
      }
      if (discardCards) {
        discardCards.unmount()
      }
      discardCards = Deck(data.playCards)
      discardCards.mount($discard)
      discardCards.cards.sort(function (a, b) {
        return a.rank - b.rank;
      });
      discardCards.showCards()
      if (typeof data.winner !== 'undefined') {
        if (player_id == data.winner) {
          $playname.style.color = '#FFBE3B'
          $playname.textContent = "Player" + player_id + " Winner !!!"
        } else {
          $playname.style.color = '#818181'
          $playname.textContent = "Player" + player_id + " Lose !!!"
        }
        $topbar.appendChild($ready)
        $bottombar.removeChild($play)
        $topbar.removeChild($pass)
      }
    }
  }
  else if (data.type == "pass") {
    cur_player_id = data.cur_player_id
    change_name_color()
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


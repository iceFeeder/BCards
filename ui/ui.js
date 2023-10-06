var prefix = Deck.prefix
var transform = prefix('transform')
var translate = Deck.translate

var $container = document.getElementById('container')
var $topbar = document.getElementById('topbar')
var $discard = document.getElementById('discard')
var $bottombar = document.getElementById('bottombar')
var $sysinfo = document.getElementById('sysinfo')

var $ready = document.createElement('button')
var $play = document.createElement('button')
var $pass = document.createElement('button')
var $playname = document.createElement('div')
var $playinfos = []

$ready.textContent = 'Ready'
$play.textContent = 'Play'
$pass.textContent = 'Pass'

$topbar.appendChild($ready)
$bottombar.appendChild($playname)

var deck = null;
var discardCards = null;

// create WebSocket connection
if (!window.WebSocket && window.MozWebSocket) {
  window.WebSocket = window.MozWebSocket;
}
var ws = new WebSocket('ws://192.168.3.9:8080/websocket');
var player_id;
var cur_player_id;

function change_name_color() {
  if (cur_player_id == player_id) {
    $playname.style.color = '#33cd3c'
  } else {
    $playname.style.color = '#fff'
  }
}

function game_start() {
  if (discardCards != null) {
    discardCards.unmount()
    discardCards = null
  }
  $topbar.removeChild($ready)
  $topbar.appendChild($pass)
  $bottombar.appendChild($play)
  $bottombar.appendChild($playname)
}

function gen_players_info(player_cards) {
  for (var i = 0; i < player_cards.length; ++i) {
    var $pinfo = document.createElement('div')
    $pinfo.textContent = "Player" + i + ": " + player_cards[i]
    if (i == cur_player_id) {
      $pinfo.style.color = '#33cd3c'
    } else {
      $pinfo.style.color = '#333333'
    }
    $sysinfo.appendChild($pinfo)
    $playinfos.push($pinfo)
  }
}

function update_players_info(player_cards) {
  for (var i = 0; i < player_cards.length; ++i) {
    $playinfos[i].textContent = "Player" + i + ": " + player_cards[i]
    if (i == cur_player_id) {
      $playinfos[i].style.color = '#33cd3c'
    } else {
      $playinfos[i].style.color = '#333333'
    }
  }
}

function poker(data) {
  if (deck != null) {
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
}

function discard_cards(cards) {
  if (discardCards != null) {
    discardCards.unmount()
  }
  discardCards = Deck(cards)
  discardCards.mount($discard)
  discardCards.cards.sort(function (a, b) {
    return a.rank - b.rank;
  });
  discardCards.showCards()
}

function game_over(winner) {
  if (player_id == winner) {
    $playname.style.color = '#FFBE3B'
    $playname.textContent = "Player" + player_id + " Winner !!!"
  } else {
    $playname.style.color = '#818181'
    $playname.textContent = "Player" + player_id + " Lose !!!"
  }
  $topbar.appendChild($ready)
  $topbar.removeChild($pass)
  $bottombar.removeChild($play)
  for (var i = 0; i < $playinfos.length; ++i) {
    $sysinfo.removeChild($playinfos[i])
  }
  $playinfos = []
}

function send_msg(action, data) {
  var msg = {}
  msg.action = action
  msg.data = data
  msg = JSON.stringify(msg)
  ws.send(msg);
}

ws.onopen = function(evt) {
}

ws.onmessage = function(evt) {
  var data = JSON.parse(evt.data);
  if (data.type == "ready") {
    if (data.start) {
      $bottombar.removeChild($playname)
      poker(data)
      cur_player_id = data.cur_player_id
      change_name_color()
      game_start()
      gen_players_info(data.player_cards)
    }
  }
  else if (data.type == "play") {
    console.log(data.playCards)
    if (data.playCards.length > 0) {
      cur_player_id = data.cur_player_id
      change_name_color()
      if (player_id == data.player_id) {
        deck.playPost()
      }
      discard_cards(data.playCards)
      update_players_info(data.player_cards)
      if (typeof data.winner !== 'undefined') {
        game_over(data.winner)
      }
    }
  }
  else if (data.type == "pass") {
    cur_player_id = data.cur_player_id
    change_name_color()
  }
}

$ready.addEventListener('click', function() {
  send_msg("ready", "")
})

$play.addEventListener('click', function() {
  if (cur_player_id != player_id) {
    return
  }
  deck.play()
  var data = {}
  data.playCards = deck.playCards
  send_msg("post_cards", data)
})

$pass.addEventListener('click', function() {
  if (cur_player_id != player_id) {
    return
  }
  send_msg("pass_turn", "")
})


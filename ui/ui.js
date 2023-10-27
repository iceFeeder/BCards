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
var $add_com = document.createElement('button')
var $playname = document.createElement('div')
var $playinfos = []

$ready.textContent = 'Ready'
$play.textContent = 'Play'
$pass.textContent = 'Pass'
$add_com.textContent = 'Add Computer'

$topbar.appendChild($ready)
$topbar.appendChild($add_com)
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
var pre_player_id;

function change_name_color() {
  if (cur_player_id == player_id) {
    $playname.style.color = '#33cd3c'
  } else {
    $playname.style.color = '#fff'
  }
  for (var i = 0; i < $playinfos.length; ++i) {
    if (i == cur_player_id) {
      $playinfos[i].style.color = '#33cd3c'
    } else {
      $playinfos[i].style.color = '#333333'
    }
  }
}

function game_start() {
  if (discardCards != null) {
    discardCards.unmount()
    discardCards = null
  }
  $topbar.removeChild($ready)
  if ($add_com != null) {
    $topbar.removeChild($add_com)
    $add_com = null
  }
  $topbar.appendChild($pass)
  $bottombar.appendChild($play)
  $bottombar.appendChild($playname)
}

function gen_players_info(player_cards, player_scores) {
  for (var i = 0; i < player_cards.length; ++i) {
    var $pinfo = document.createElement('div')
    if (i == cur_player_id) {
      $pinfo.style.color = '#33cd3c'
    } else {
      $pinfo.style.color = '#333333'
    }
    $sysinfo.appendChild($pinfo)
    $playinfos.push($pinfo)
  }
}

function update_players_info(player_cards, player_scores) {
  for (var i = 0; i < player_cards.length; ++i) {
    if (i == pre_player_id) {
      $playinfos[i].textContent = "P" + i + "[" + player_cards[i]+ "]" + ": " + player_scores[i] + " <-"
    } else {
      $playinfos[i].textContent = "P" + i + "[" + player_cards[i]+ "]" + ": " + player_scores[i]
    }
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

function update_players(data) {
  players = data.players
  for (var i = 0; i < players.length; ++i) {
    if (i >= $playinfos.length) {
      var $pinfo = document.createElement('div')
      $playinfos.push($pinfo)
      $sysinfo.appendChild($pinfo)
    }
    $playinfos[i].textContent = players[i].name
    if (players[i].ready == 1) {
      $playinfos[i].style.color = '#33cd3c'
    } else {
      $playinfos[i].style.color = '#333333'
    }
  }
}

ws.onmessage = function(evt) {
  var data = JSON.parse(evt.data);
  if (data.type == "init") {
    update_players(data)
  }
  else if (data.type == "ready") {
    if (data.start) {
      $bottombar.removeChild($playname)
      poker(data)
      cur_player_id = data.cur_player_id
      change_name_color()
      game_start()
      update_players_info(data.player_cards, data.player_scores)
    } else {
      update_players(data)
    }
  }
  else if (data.type == "play") {
    console.log(data.playCards)
    if (data.playCards.length > 0) {
      cur_player_id = data.cur_player_id
      pre_player_id = data.pre_player_id
      change_name_color()
      if (player_id == data.player_id) {
        deck.playPost()
      }
      discard_cards(data.playCards)
      update_players_info(data.player_cards, data.player_scores)
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

$add_com.addEventListener('click', function() {
  send_msg("add_com", "")
})

$pass.addEventListener('click', function() {
  if (cur_player_id != player_id) {
    return
  }
  send_msg("pass_turn", "")
})


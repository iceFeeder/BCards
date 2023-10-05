'use strict';

var Deck = (function () {
  'use strict';

  var style = document.createElement('p').style;
  var memoized = {};

  function prefix(param) {
    if (typeof memoized[param] !== 'undefined') {
      return memoized[param];
    }

    if (typeof style[param] !== 'undefined') {
      memoized[param] = param;
      return param;
    }

    var camelCase = param[0].toUpperCase() + param.slice(1);
    var prefixes = ['webkit', 'moz', 'Moz', 'ms', 'o'];
    var test;

    for (var i = 0, len = prefixes.length; i < len; i++) {
      test = prefixes[i] + camelCase;
      if (typeof style[test] !== 'undefined') {
        memoized[param] = test;
        return test;
      }
    }
  }

  function translate(a, b) {
    return 'translate(' + a + ', ' + b + ')';
  }

  function createElement(type) {
    return document.createElement(type);
  }

  function _card(i) {
    var transform = prefix('transform');

    // calculate rank/suit, etc..
    var rank = i % 13 + 1;
    var suit = i / 13 | 0;
    var z = (52 - i) / 4;

    // create elements
    var $el = createElement('div');
    var $face = createElement('div');
    var $back = createElement('div');

    // states
    var isSelected = false;

    // self = card
    var self = { i: i, rank: rank, suit: suit, pos: i, $el: $el, mount: mount, unmount: unmount, setSide: setSide,isSelected:isSelected };

    var modules = Deck.modules;
    var module;

    // add classes
    $face.classList.add('face');
    $back.classList.add('back');

    // add default transform
    $el.style[transform] = translate(-z + 'px', -z + 'px');

    // add default values
    self.x = -z;
    self.y = -z;
    self.z = z;
    self.rot = 0;

    // set default side to back
    self.setSide('back');

    // add drag/click listeners
    addListener($el, 'mousedown', onMousedown);

    // load modules
    for (module in modules) {
      addModule(modules[module]);
    }

    // set rank & suit
    self.setRankSuit = function (rank, suit) {
      var suitName = SuitName(suit);
      $el.setAttribute('class', 'card ' + suitName + ' rank' + rank);
    };

    self.setRankSuit(rank, suit);

    return self;

    function addModule(module) {
      // add card module
      module.card && module.card(self);
    }

    function onMousedown(e) {
      var pos = 0;

      e.preventDefault();

      if (!self.isSelected){
        pos = -10;
      }
      self.isSelected = !self.isSelected;
      $el.style[transform] = translate(self.x + 'px', Math.round(self.y + pos) + 'px');
    }

    function mount(target) {
      // mount card to target (deck)
      target.appendChild($el);

      self.$root = target;
    }

    function unmount() {
      // unmount from root (deck)
      self.$root && self.$root.removeChild($el);
      self.$root = null;
    }

    function setSide(newSide) {
      // flip sides
      if (newSide === 'front') {
        if (self.side === 'back') {
          $el.removeChild($back);
        }
        self.side = 'front';
        $el.appendChild($face);
        self.setRankSuit(self.rank, self.suit);
      } else {
        if (self.side === 'front') {
          $el.removeChild($face);
        }
        self.side = 'back';
        $el.appendChild($back);
        $el.setAttribute('class', 'card');
      }
    }
  }

  function SuitName(suit) {
    // return suit name from suit value
    return suit === 0 ? 'spades' : suit === 1 ? 'hearts' : suit === 2 ? 'clubs' : suit === 3 ? 'diamonds' : 'joker';
  }

  function addListener(target, name, listener) {
    target.addEventListener(name, listener);
  }

  function removeListener(target, name, listener) {
    target.removeEventListener(name, listener);
  }

  function fontSize() {
    return window.getComputedStyle(document.body).getPropertyValue('font-size').slice(0, -2);
  }

  var __fontSize;

  var poker = {
    deck: function deck(_deck4) {
      _deck4.poker = _deck4.queued(poker);

      function poker(next) {
        var cards = _deck4.cards;
        var len = cards.length;

        __fontSize = fontSize();

        cards.forEach(function (card, i) {
          card.poker(i, len, function (i) {
            card.setSide('front');
            if (i === cards.length - 1) {
              next();
            }
          });
        });
      }
    },
    card: function card(_card4) {
      var $el = _card4.$el;

      _card4.poker = function (i, len, cb) {
        var delay = i * 250;
        $el.style.zIndex = len - 1 + i;
        _card4.x = Math.round((i - 2.05) * 10 * __fontSize / 16);
        _card4.y = Math.round(-110 * __fontSize / 16)+300;
        $el.style[transform] = translate(_card4.x + 'px', _card4.y + 'px');
        cb(i);
      };
    }
  };

  var ___fontSize;

  var playPost = {
    deck:function deck(_deck5){
      _deck5.playPost = _deck5.queued(playPost);
      function playPost(next){
        var cards = _deck5.cards;
        var select = [];
        var remain = [];
        cards.forEach(function (card) {
          if(card.isSelected) {
            select.push(card)
          }else {
            remain.push(card)
          }
        });

        _deck5.cards = remain

        ___fontSize = fontSize();

        select.forEach(function (card, i) {
          card.unmount()
          if (i === select.length - 1) {
            next();
          }
        });

        remain.forEach(function (card,i) {
          card.playPost(i, remain.length, function (){
            if (i === remain.length - 1) {
              next();
            }
          });
        });
      }
    },
    card:function card(_card5){
      var $el = _card5.$el;
      _card5.playPost = function (i,len, cb) {
        _card5.animateTo({
          delay: 0,
          duration: 250,

          x: Math.round((i - 2.05) * 10 * ___fontSize / 16),
          y: Math.round(-110 * ___fontSize / 16)+300,
          rot: 0,
          onStart: function onStart() {
            $el.style.zIndex = len - 1 + i;
          },
          onComplete: function onComplete() {
            cb(i);
          }
        });
      };
    }
  }

  var play = {
    deck:function deck(_deck6){
      _deck6.play = _deck6.queued(play);
      function play(next){
        var cards = _deck6.cards;
        var select = [];
        cards.forEach(function (card,i) {
          if(card.isSelected) {
            select.push(card.i)
          }
        });
        _deck6.post = select
        next()
      }
    },
  }

  var ____fontSize;

  var showCards = {
    deck:function deck(_deck7){
      _deck7.showCards = _deck7.queued(showCards);
      function showCards(next, data){
        var _cards = data.postCards;
        var len = _cards.length;
        var cards = new Array(len);

        var card;
        for (var i = _cards.length; i; i--){
          card = cards[i - 1] = _card(_cards[i - 1]);
          card.setSide('front');
          card.mount(_deck7.$el);
        }

        ____fontSize = fontSize();

        cards.forEach(function (card,i) {
          card.showCards(i, cards.length, data.index, function (){
            if (i === cards.length - 1) {
              next();
            }
          });
        });
      }
    },
    card:function card(_card7){
      var $el = _card7.$el;
      _card7.showCards = function (i,len,index, cb) {
        _card7.animateTo({
          delay: 0,
          duration: 250,

          x: Math.round((i - 2.05) * 10 * ____fontSize / 16),
          y: -200,
          rot: 0,
          onStart: function onStart() {
            $el.style.zIndex = len - 1 + i;
          },
          onComplete: function onComplete() {
            cb(i);
          }
        });
      };
    }
  }

  function queue(target) {
    var array = Array.prototype;
    var queueing = [];

    target.queue = queue;
    target.queued = queued;

    return target;

    function queued(action) {
      return function () {
        var self = this;
        var args = arguments;

        queue(function (next) {
          action.apply(self, array.concat.apply(next, args));
        });
      };
    }

    function queue(action) {
      if (!action) {
        return;
      }

      queueing.push(action);

      if (queueing.length === 1) {
        next();
      }
    }
    function next() {
      queueing[0](function (err) {
        if (err) {
          throw err;
        }

        queueing = queueing.slice(1);

        if (queueing.length) {
          next();
        }
      });
    }
  }

  function observable(target) {
    target || (target = {});
    var listeners = {};

    target.on = on;
    target.one = one;
    target.off = off;
    target.trigger = trigger;

    return target;

    function on(name, cb, ctx) {
      listeners[name] || (listeners[name] = []);
      listeners[name].push({ cb: cb, ctx: ctx });
    }

    function one(name, cb, ctx) {
      listeners[name] || (listeners[name] = []);
      listeners[name].push({
        cb: cb, ctx: ctx, once: true
      });
    }

    function trigger(name) {
      var self = this;
      var args = Array.prototype.slice(arguments, 1);

      var currentListeners = listeners[name] || [];

      currentListeners.filter(function (listener) {
        listener.cb.apply(self, args);

        return !listener.once;
      });
    }

    function off(name, cb) {
      if (!name) {
        listeners = {};
        return;
      }

      if (!cb) {
        listeners[name] = [];
        return;
      }

      listeners[name] = listeners[name].filter(function (listener) {
        return listener.cb !== cb;
      });
    }
  }

  function Deck(data) {
    // init cards array
    var __cards = data;
    var cards = new Array(__cards.length);
    var $el = createElement('div');
    var self = observable({ mount: mount, unmount: unmount, cards: cards, $el: $el, prePost: [] });
    var $root;

    var modules = Deck.modules;
    var module;

    // make queueable
    queue(self);

    // load modules
    for (module in modules) {
      addModule(modules[module]);
    }

    // add class
    $el.classList.add('deck');

    var card;
    for (var i = __cards.length; i; i--){
       card = cards[i - 1] = _card(__cards[i - 1]);
       card.mount($el);
    }

    return self;

    function mount(root) {
      // mount deck to root
      $root = root;
      $root.appendChild($el);
    }

    function unmount() {
      // unmount deck from root
      $root.removeChild($el);
    }

    function addModule(module) {
      module.deck && module.deck(self);
    }
  }
  Deck.modules = { poker: poker, play: play, playPost: playPost, showCards: showCards};
  Deck.Card = _card;
  Deck.prefix = prefix;
  Deck.translate = translate;

  return Deck;
})();

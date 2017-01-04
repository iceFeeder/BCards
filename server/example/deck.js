'use strict';

var Deck = (function () {
  'use strict';

  var ticking;
  var animations = [];

  function animationFrames(delay, duration) {
    var now = Date.now();

    // calculate animation start/end times
    var start = now + delay;
    var end = start + duration;

    var animation = {
      start: start,
      end: end
    };

    // add animation
    animations.push(animation);

    if (!ticking) {
      // start ticking
      ticking = true;
      requestAnimationFrame(tick);
    }
    var self = {
      start: function start(cb) {
        // add start callback (just one)
        animation.startcb = cb;
        return self;
      },
      progress: function progress(cb) {
        // add progress callback (just one)
        animation.progresscb = cb;
        return self;
      },
      end: function end(cb) {
        // add end callback (just one)
        animation.endcb = cb;
        return self;
      }
    };
    return self;
  }

  function tick() {
    var now = Date.now();

    if (!animations.length) {
      // stop ticking
      ticking = false;
      return;
    }

    for (var i = 0, animation; i < animations.length; i++) {
      animation = animations[i];
      if (now < animation.start) {
        // animation not yet started..
        continue;
      }
      if (!animation.started) {
        // animation starts
        animation.started = true;
        animation.startcb && animation.startcb();
      }
      // animation progress
      var t = (now - animation.start) / (animation.end - animation.start);
      animation.progresscb && animation.progresscb(t < 1 ? t : 1);
      if (now > animation.end) {
        // animation ended
        animation.endcb && animation.endcb();
        animations.splice(i--, 1);
        continue;
      }
    }
    requestAnimationFrame(tick);
  }

  // fallback
  window.requestAnimationFrame || (window.requestAnimationFrame = function (cb) {
    setTimeout(cb, 0);
  });

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

  var has3d;

  function translate(a, b, c) {
    typeof has3d !== 'undefined' || (has3d = check3d());

    c = c || 0;

    if (has3d) {
      return 'translate3d(' + a + ', ' + b + ', ' + c + ')';
    } else {
      return 'translate(' + a + ', ' + b + ')';
    }
  }

  function check3d() {
    // I admit, this line is stealed from the great Velocity.js!
    // http://julian.com/research/velocity/
    var isMobile = /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);

    if (!isMobile) {
      return false;
    }

    var transform = prefix('transform');
    var $p = document.createElement('p');

    document.body.appendChild($p);
    $p.style[transform] = 'translate3d(1px,1px,1px)';

    has3d = $p.style[transform];
    has3d = has3d != null && has3d.length && has3d !== 'none';

    document.body.removeChild($p);

    return has3d;
  }

  function createElement(type) {
    return document.createElement(type);
  }

  var maxZ = 52;

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

    self.animateTo = function (params) {
      var delay = params.delay;
      var duration = params.duration;
      var _params$x = params.x;
      var x = _params$x === undefined ? self.x : _params$x;
      var _params$y = params.y;
      var y = _params$y === undefined ? self.y : _params$y;
      var _params$rot = params.rot;
      var rot = _params$rot === undefined ? self.rot : _params$rot;
      var ease$$ = params.ease;
      var onStart = params.onStart;
      var onProgress = params.onProgress;
      var onComplete = params.onComplete;

      var startX, startY, startRot;
      var diffX, diffY, diffRot;

      animationFrames(delay, duration).start(function () {
        startX = self.x || 0;
        startY = self.y || 0;
        startRot = self.rot || 0;
        onStart && onStart();
      }).progress(function (t) {
        var et = ease[ease$$ || 'cubicInOut'](t);

        diffX = x - startX;
        diffY = y - startY;
        diffRot = rot - startRot;

        onProgress && onProgress(t, et);

        self.x = startX + diffX * et;
        self.y = startY + diffY * et;
        self.rot = startRot + diffRot * et;

        $el.style[transform] = translate(self.x + 'px', self.y + 'px') + (diffRot ? 'rotate(' + self.rot + 'deg)' : '');
      }).end(function () {
        onComplete && onComplete();
      });
    };

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
      $el.style[transform] = translate(self.x + 'px', Math.round(self.y + pos) + 'px') + (self.rot ? ' rotate(' + self.rot + 'deg)' : '');
      //$el.style.zIndex = maxZ++;
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

  var ease = {
    linear: function linear(t) {
      return t;
    },
    quadIn: function quadIn(t) {
      return t * t;
    },
    quadOut: function quadOut(t) {
      return t * (2 - t);
    },
    quadInOut: function quadInOut(t) {
      return t < 0.5 ? 2 * t * t : -1 + (4 - 2 * t) * t;
    },
    cubicIn: function cubicIn(t) {
      return t * t * t;
    },
    cubicOut: function cubicOut(t) {
      return --t * t * t + 1;
    },
    cubicInOut: function cubicInOut(t) {
      return t < 0.5 ? 4 * t * t * t : (t - 1) * (2 * t - 2) * (2 * t - 2) + 1;
    },
    quartIn: function quartIn(t) {
      return t * t * t * t;
    },
    quartOut: function quartOut(t) {
      return 1 - --t * t * t * t;
    },
    quartInOut: function quartInOut(t) {
      return t < 0.5 ? 8 * t * t * t * t : 1 - 8 * --t * t * t * t;
    },
    quintIn: function quintIn(t) {
      return t * t * t * t * t;
    },
    quintOut: function quintOut(t) {
      return 1 + --t * t * t * t * t;
    },
    quintInOut: function quintInOut(t) {
      return t < 0.5 ? 16 * t * t * t * t * t : 1 + 16 * --t * t * t * t * t;
    }
  };


  var sort = {
    deck: function deck(_deck2) {
      _deck2.sort = _deck2.queued(sort);

      function sort(next, type) {
        var cards = _deck2.cards;

        cards.sort(function (a, b) {
          if (type == 1){
            return a.i - b.i
          }else {
            return a.rank - b.rank;
          }
        });

        cards.forEach(function (card, i) {
          card.sort(i, cards.length, function (i) {
            if (i === cards.length - 1) {
              next();
            }
          }, type);
        });
      }
    },
    card: function card(_card2) {
      var $el = _card2.$el;

      _card2.sort = function (i, len, cb, type) {
        var z = i / 4;
        var delay = i * 10;

        _card2.animateTo({
          delay: delay,
          duration: 400,

          x: -z,
          y: -150,
          rot: 0,

          onComplete: function onComplete() {
            $el.style.zIndex = i;
          }
        });

        _card2.animateTo({
          delay: delay + 500,
          duration: 400,

          x: -z,
          y: -z,
          rot: 0,

          onComplete: function onComplete() {
            cb(i);
          }
        });
      };
    }
  };

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

        _card4.animateTo({
          delay: delay,
          duration: 250,

          x: Math.round((i - 2.05) * 10 * __fontSize / 16),
          y: Math.round(-110 * __fontSize / 16)+300,
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
  };

  var ___fontSize;

  var play = {
    deck:function deck(_deck5){
      _deck5.play = _deck5.queued(play);
      function play(next){
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
        _deck5.post = select

        ___fontSize = fontSize();

        select.forEach(function (card, i) {
          card.unmount()
          if (i === select.length - 1) {
            next();
          }
        });

        remain.forEach(function (card,i) {
          card.play(i,remain.length,function (){
            if (i === remain.length - 1) {
              next();
            }
          });
        });
      }
    },
    card:function card(_card5){
      var $el = _card5.$el;
      _card5.play = function (i,len, cb) {
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
    var self = observable({ mount: mount, unmount: unmount, cards: cards, $el: $el });
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
  Deck.animationFrames = animationFrames;
  Deck.ease = ease;
  Deck.modules = { poker: poker, sort: sort, play: play};
  Deck.Card = _card;
  Deck.prefix = prefix;
  Deck.translate = translate;
  Deck.pre = []

  return Deck;
})();

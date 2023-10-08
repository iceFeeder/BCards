from cardspool import CardsPool
from gcore.bcards.bcard import BCard
from card import Cards, CardsType
import random


class BCards(CardsPool):
    def __init__(self):
        super(BCards, self).__init__(size=52)
        self.pre_cards = None
        self.cur_cards = None
        self.max_players = 4
        self.cur_player = None
        self.player_num = None
        self.pre_player = None
        self.player_cards = None
        self.ok = set()
        self.player_scores = None

    def pass_player(self, player_id):
        if player_id != self.cur_player or player_id == self.pre_player:
            return False
        self.pre_cards = None
        self.cur_player = (self.cur_player + 1) % self.player_num
        return True

    def update_player(self):
        self.pre_player = self.cur_player
        self.cur_player = (self.cur_player + 1) % self.player_num

    def get_cards(self, index=0):
        index = int(index) % 4
        return self.pool[index::4]

    def ready(self, player_id, players):
        self.ok.add(player_id)
        if len(self.ok) == len(players) and len(self.ok) != 1:
            self.cur_player = random.randint(0, len(self.ok) - 1)
            self.player_num = len(self.ok)
            self.player_cards = [13] * self.player_num
            if self.player_scores is None:
                self.player_scores = [0] * self.player_num
            return True
        return False

    def game_over(self):
        print("player cards: ", self.player_cards)
        for i in range(len(self.player_cards)):
            if self.player_cards[i] == 0:
                self.player_scores = list(map(lambda a: a[0] + (a[1] if a[1] < 10 else a[1] * 2),
                                              zip(self.player_scores, self.player_cards)))
                return i
        return -1

    def is_valid(self, cards):
        num = len(cards)
        if num > 5 or num == 0:
            return False
        cs = Cards()
        for v in cards:
            c = BCard(v)
            cs.cards.append(c)
            cs.values[c.val] += 1
            cs.suits[c.suit] += 1
            cs.num += 1
        if cs.num < 5:
            if len(cs.values) != 1:
                return False
            cs.type = CardsType.NoFive
            cs.priority = cs.cards[0].rank * 10 + cs.cards[0].suit
        else:
            if len(cs.values) == 5:
                start = None
                for r in range(1, 10):
                    if r in cs.values:
                        start = r
                        break
                for r in range(start + 1, start + 5):
                    if r == 13:
                        r = 0
                    if r not in cs.values:
                        break
                else:
                    cs.type = CardsType.Straight
                    cs.priority = BCard.PRIORITY_RANK[(start + 4) % 13]
                if len(cs.suits) == 1:
                    if cs.type == CardsType.Straight:
                        cs.type = CardsType.FlushStraight
                    else:
                        cs.type = CardsType.Flush
                    cs.priority += (cs.cards[0].suit + 1) * 100
                if cs.type is None:
                    return False
            elif len(cs.values) == 2:
                for card, cnts in cs.values.items():
                    if cnts == 3:
                        cs.type = CardsType.FullHouse
                        cs.priority = BCard.PRIORITY_RANK[card]
                    if cnts == 4:
                        cs.type = CardsType.Quads
                        cs.priority = BCard.PRIORITY_RANK[card]
            else:
                return False
        cs.priority += int(cs.type) * 1000
        self.cur_cards = cs
        return True

    def check(self, play_cards, player_id):
        print(self.pre_cards, play_cards)
        if not self.is_valid(play_cards):
            return False
        if self.pre_cards and self.pre_cards.num != len(play_cards):
            return False
        if not self.pre_cards:
            ret = True
        else:
            print("pre: ", self.pre_cards,
                  "cur: ", self.cur_cards)
            ret = self.pre_cards.priority < self.cur_cards.priority

        if ret:
            self.pre_cards = self.cur_cards
            self.cur_cards = None
            self.player_cards[player_id] -= len(play_cards)
        return ret

    def reset(self):
        self.clear()
        super(BCards, self).reset()

    def reset_scores(self):
        self.player_scores = None

    def clear(self):
        self.pre_cards = None
        self.cur_cards = None
        self.cur_player = None
        self.player_num = None
        self.pre_player = None
        self.player_cards = None
        self.ok = set()

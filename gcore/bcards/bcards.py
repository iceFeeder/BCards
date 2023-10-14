from cardspool import CardsPool
from gcore.bcards.bcard import BCard
from card import Cards, CardsType
from gcore.player import PlayerType


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
        self.pre_winner = None

    def pass_player(self, player_id):
        if player_id != self.cur_player or player_id == self.pre_player:
            return False
        self.cur_player = (self.cur_player + 1) % self.player_num
        return True

    def update_player(self):
        self.pre_player = self.cur_player
        self.cur_player = (self.cur_player + 1) % self.player_num

    def get_cards(self, index=0):
        index = int(index) % 4
        return self.pool[index::4]

    def get_priority(self, card):
        return BCard(card).priority

    def get_init_player(self, players):
        if self.pre_winner is not None:
            return self.pre_winner
        min_card = float("inf")
        init_player = 0
        for i in range(len(players)):
            cards = self.get_cards(i)
            for c in cards:
                if self.get_priority(c) < min_card:
                    init_player = i
        return init_player

    def ready(self, player_id, players):
        self.ok.add(player_id)
        if len(self.ok) == len(players) and len(self.ok) != 1:
            self.cur_player = self.get_init_player(players)
            self.player_num = len(self.ok)
            self.player_cards = [13] * self.player_num
            if self.player_scores is None:
                self.player_scores = [0] * self.player_num
            return True
        return False

    def game_over(self):
        def get_score(pp):
            pre_score = pp[0]
            cards = pp[1]
            if cards < 10:
                return pre_score + cards
            elif cards < 13:
                return pre_score + cards * 2
            elif cards == 13:
                return pre_score + cards * 3
        for i in range(len(self.player_cards)):
            if self.player_cards[i] == 0:
                self.player_scores = \
                    list(map(get_score, zip(self.player_scores, self.player_cards)))
                return i
        return -1

    def is_valid(self, cards):
        num = len(cards)
        if num > 5 or num == 0:
            return None
        cs = Cards()
        for v in cards:
            c = BCard(v)
            cs.cards.append(c)
            cs.raw_cards.append(v)
            cs.values[c.val] += 1
            cs.suits[c.suit] += 1
        if num < 5:
            if len(cs.values) != 1:
                return None
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
                    return None
            elif len(cs.values) == 2:
                for card, cnts in cs.values.items():
                    if cnts == 3:
                        cs.type = CardsType.FullHouse
                        cs.priority = BCard.PRIORITY_RANK[card]
                    if cnts == 4:
                        cs.type = CardsType.Quads
                        cs.priority = BCard.PRIORITY_RANK[card]
            else:
                return None
        cs.priority += int(cs.type) * 1000
        return cs

    def check_pre_player(self, player_id):
        if player_id == self.pre_player:
            self.pre_cards = None

    def check(self, play_cards, player_id):
        self.check_pre_player(player_id)
        self.cur_cards = self.is_valid(play_cards)
        if not self.cur_cards:
            return False
        if self.pre_cards and len(self.pre_cards.cards) != len(play_cards):
            return False
        if not self.pre_cards:
            ret = True
        else:
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
        self.pre_winner = None

    def com_ready(self, players):
        for p in players:
            if p.type == PlayerType.Computer:
                p.processor.ready()
            else:
                p.ready = 0

    def clear(self):
        self.pre_cards = None
        self.cur_cards = None
        self.cur_player = None
        self.player_num = None
        self.pre_player = None
        self.player_cards = None
        self.ok = set()

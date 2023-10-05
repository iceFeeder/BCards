from cardspool import CardsPool
from gcore.bcards.bcard import BCard
from card import Cards, CardsType


class BCards(CardsPool):
    def __init__(self):
        super(BCards, self).__init__(size=52)
        self.pre_cards = None
        self.cur_cards = None
        self.max_players = 4

    def get_cards(self, index=0):
        index = int(index) % 4
        return self.pool[index::4]

    def is_valid(self, cards):
        num = len(cards)
        if num > 5 or num == 0:
            return False
        cs = Cards()
        for v in cards:
            c = BCard(v)
            cs.cards.append(c)
            cs.values[c.rank] += 1
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
                    cs.type = CardsType.FlushStraight
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

    def check(self, play_cards):
        print(self.pre_cards, play_cards)
        if not self.is_valid(play_cards):
            return False
        if self.pre_cards and self.pre_cards.num != len(play_cards):
            return False
        if not self.pre_cards:
            ret = True
        else:
            ret = self.pre_cards.priority < self.cur_cards.priority

        if ret:
            self.pre_cards = self.cur_cards
            self.cur_cards = None
        print("OK", self.pre_cards)
        return ret

    def reset(self):
        self.clear()
        super(BCards, self).reset()

    def clear(self):
        self.pre_cards = None


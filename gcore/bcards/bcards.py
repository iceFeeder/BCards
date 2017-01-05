from cardspool import CardsPool
from gcore.bcards.bcard import BCard

class BCards(CardsPool):
    def __init__(self):
        super(BCards,self).__init__(size=52)

    def check_cards(self,data):
        print data
        pre , post = data['pre_post'], data['cards']

        if pre!=[] and (len(pre) != len(post)):
            return False
        pre_val = self._get_priority(pre)
        post_val = self._get_priority(post)
        if post_val > pre_val:
            return True
        return False

    def _get_priority(self,cards):
        num = len(cards)
        if num > 5 : return -1
        if num == 0 : return 0

        sorted(cards,key=lambda card:card % 13)

        ranks = [0] * 13
        suits = [0] * 4
        _cards = []

        for v in cards:
            c = BCard(v)
            _cards.append(c)
            ranks[c.rank] += 1
            suits[c.suit] += 1
        if num != 5:
            if ranks[_cards[0].rank] != num:
                return -1
            return _cards[num-1].rank * 10 + _cards[num-1].suit
        return -1
        level = 0
        straight = False
        flush = False

        if ranks[_cards[0].rank] == 4 or ranks[_cards[4].rank] == 4:
            pass



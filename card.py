from enum import IntEnum
from collections import defaultdict


class Card(object):
    PRIORITY_RANK = {0: 0, 1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 6, 7: 7, 8: 8, 9: 9, 10: 10, 11: 11, 12: 12, 13: 13}
    PRIORITY_SUIT = {0: 3, 1: 2, 2: 1, 3: 0, 4: 4}

    def __init__(self, val):
        self.val = val % 13
        self.rank = self.PRIORITY_RANK[val % 13]
        self.suit = self.PRIORITY_SUIT[val // 13]

    def __str__(self):
        return "({}, {})".format(self.val, self.suit)


class CardsType(IntEnum):
    NoFive = 0
    Straight = 1
    Flush = 2
    FullHouse = 3
    Quads = 4
    FlushStraight = 5


class Cards(object):
    def __init__(self):
        self.values = defaultdict(int)
        self.suits = defaultdict(int)
        self.type = None
        self.priority = 0
        self.cards = []

    def __str__(self):
        return ' '.join(map(str, self.cards)) + \
               "\nPriority: " + str(self.priority) + \
               "\nType: " + str(int(self.type))


from enum import IntEnum
from collections import defaultdict
from functools import total_ordering


class Card(object):
    PRIORITY_RANK = {0: 0, 1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 6, 7: 7, 8: 8, 9: 9, 10: 10, 11: 11, 12: 12, 13: 13}
    PRIORITY_SUIT = {0: 3, 1: 2, 2: 1, 3: 0, 4: 4}

    def __init__(self, val):
        self.val = val % 13
        self.rank = self.PRIORITY_RANK[val % 13]
        self.suit = self.PRIORITY_SUIT[val // 13]
        self.priority = self.rank * 10 + self.suit

    def __str__(self):
        return "({}, {}, {})".format(self.val, self.suit, self.priority)


class CardsType(IntEnum):
    NoFive = 0
    Straight = 1
    Flush = 2
    FullHouse = 3
    Quads = 4
    FlushStraight = 5


@total_ordering
class Cards(object):
    def __init__(self):
        self.values = defaultdict(int)
        self.suits = defaultdict(int)
        self.type = None
        self.priority = 0
        self.cards = []
        self.raw_cards = []

    def __str__(self):
        return ' '.join(map(str, self.cards)) + \
               "\nPriority: " + str(self.priority) + \
               "\nType: " + str(int(self.type))

    def __eq__(self, other):
        return self.priority == other.priority

    def __lt__(self, other):
        return self.priority < other.priority

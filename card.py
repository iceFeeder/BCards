from enum import IntEnum
from collections import defaultdict
from functools import total_ordering


@total_ordering
class Card(object):
    PRIORITY_RANK = {0: 0, 1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 6, 7: 7, 8: 8, 9: 9, 10: 10, 11: 11, 12: 12, 13: 13}
    PRIORITY_SUIT = {0: 4, 1: 3, 2: 2, 3: 1, 4: 5}
    SUIT_TO_PRINT = {
        0: '♠',
        1: '♥',
        2: '♣',
        3: '♦',
        4: '🃏'
    }
    VAL_TO_NAME = {
        0: 'A',
        1: '2',
        2: '3',
        3: '4',
        4: '5',
        5: '6',
        6: '7',
        7: '8',
        8: '9',
        9: '10',
        10: 'J',
        11: 'Q',
        12: 'K',

    }

    def __init__(self, val):
        self.val = val % 13
        self.suit = val // 13
        self.rank = self.PRIORITY_RANK[self.val]
        self.suit_rank = self.PRIORITY_SUIT[self.suit]
        self.name = self.VAL_TO_NAME[self.val]
        self.suit_name = self.SUIT_TO_PRINT[self.suit]
        self.priority = self.rank * 10 + self.suit_rank

    def __str__(self):
        return "<{}{}>".format(self.suit_name, self.name)

    def __eq__(self, other):
        return self.rank == other.rank

    def __lt__(self, other):
        return self.rank < other.rank


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
        return ''.join(map(str, self.cards))

    def __eq__(self, other):
        return self.priority == other.priority

    def __lt__(self, other):
        return self.priority < other.priority


def str_cards_list(cards_list):
    return "[" + ','.join(map(str, cards_list)) + "]"


def print_raw_cards(raw_cards):
    cards = []
    for c in raw_cards:
        cards.append(Card(c))
    cards.sort()
    print(''.join(map(str, cards)))

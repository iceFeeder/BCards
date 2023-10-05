class Card(object):
    PRIORITY_RANK = {0: 0, 1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 6, 7: 7, 8: 8, 9: 9, 10: 10, 11: 11, 12: 12}
    PRIORITY_SUIT = {0: 0, 1: 1, 2: 2, 3: 3, 4: 4}

    def __init__(self, val):
        self.rank = self.PRIORITY_RANK[val % 13]
        self.suit = self.PRIORITY_SUIT[val // 13]

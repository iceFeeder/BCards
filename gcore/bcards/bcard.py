from card import Card


class BCard(Card):
    PRIORITY_RANK = {
        2: 0,    # 3
        3: 1,    # 4
        4: 2,    # 5
        5: 3,    # 6
        6: 4,    # 7
        7: 5,    # 8
        8: 6,    # 9
        9: 7,    # 10
        10: 8,   # J
        11: 9,   # Q
        12: 10,  # K
        0: 11,   # A
        1: 12,   # 2
    }

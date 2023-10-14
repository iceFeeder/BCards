import copy
import json
import time
from enum import IntEnum


class ComputerType(IntEnum):
    EASY = 1
    HARD = 2


class Computer(object):
    def __init__(self, player, server, com_type=ComputerType.EASY):
        self.player = player
        self.server = server
        self.gcore = server.gcore
        self.cards = self.gcore.get_cards(player.id)
        self.valid_cards = self.get_valid_cards()
        self.type = com_type

    def set_cards(self):
        self.cards = self.gcore.get_cards(self.player.id)
        self.valid_cards = self.get_valid_cards()

    def get_valid_cards(self):
        valid_cards = {}
        total = []
        for i in range(5, 0, -1):
            cards = self.get_cards(i, self.cards)
            cards = sorted(cards)
            total += cards
            valid_cards[i] = cards if cards else []
        valid_cards[0] = total
        return valid_cards

    def has_cards(self, cards):
        return len(set(cards) & set(self.cards)) == len(set(cards))

    def get_cards(self, n, candidates):
        cards = []
        cur = []

        def dfs(k):
            if len(cur) == n:
                valid = self.gcore.is_valid(cur)
                if valid:
                    cards.append(copy.deepcopy(valid))
            elif len(cur) < n:
                if k < len(candidates):
                    cur.append(candidates[k])
                    dfs(k + 1)
                    cur.pop()
                    dfs(k + 1)

        dfs(0)
        return cards

    def hard_computer(self):
        res, to_all = {}, None
        return res, to_all

    def easy_computer(self):
        res, to_all = {}, None
        self.gcore.check_pre_player(self.player.id)
        num = len(self.gcore.pre_cards.cards) if self.gcore.pre_cards else 0
        cards = self.valid_cards[num]
        for cs in cards:
            if not self.has_cards(cs.raw_cards):
                continue
            d = {'playCards': cs.raw_cards}
            res, to_all = self.server.post_cards(self.player.id, d)
            if res:
                print("computer " + str(self.player.id) + " play: ", res)
                if 'winner' not in res:
                    for c in cs.raw_cards:
                        self.cards.remove(c)
                break
        if not res:
            res, to_all = self.server.pass_turn(self.player.id)
            print("computer " + str(self.player.id) + " pass ...", res)
        return res, to_all

    def send(self, data):
        data = json.loads(data)
        print("computer " + str(self.player.id) + "view: ", data)
        if self.gcore.cur_player == self.player.id:
            time.sleep(2)
            res, to_all = self.easy_computer() if self.type == ComputerType.EASY else self.hard_computer()
            self.server.send_msg(res, to_all, self.player.processor)

    def ready(self):
        res, to_all = self.server.ready(self.player.id)
        self.set_cards()
        self.server.send_msg(res, to_all, self.player.processor)

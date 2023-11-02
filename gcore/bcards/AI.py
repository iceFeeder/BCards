import copy

from card import *
from gcore.bcards.bcard import BCard


class Computer(object):
    def __init__(self, player, server):
        self.player = player
        self.server = server
        self.gcore = server.gcore
        self.cards = []
        self.valid_cards = {}
        self.continue_pass = 0
        self.pre_is_pass = False
        self.split_cards = False

    def set_cards(self):
        self.cards = self.gcore.get_cards(self.player.id)
        self.split_cards = False
        self.valid_cards = self.get_valid_cards()

    def get_valid_cards(self):
        valid_cards = {}
        total = []
        tmp_cards = copy.deepcopy(self.cards)
        for i in range(5, 0, -1):
            cur_cards = self.cards if self.split_cards else tmp_cards
            cards = self.get_cards(i, cur_cards)
            cards.sort()
            final_cards = []
            for cs in cards[::-1]:
                if self.has_cards(cs.raw_cards, tmp_cards):
                    final_cards.append(cs)
                    for c in cs.raw_cards:
                        if BCard(c).rank == 12 and i != 5:
                            continue
                        tmp_cards.remove(c)
            final_cards.sort()
            new_cards = cards if self.split_cards else final_cards
            total += new_cards
            valid_cards[i] = new_cards if new_cards else []
        total.sort()
        valid_cards[0] = total
        print("Player" + str(self.player.id) + ": " + str_cards_list(total))
        return valid_cards

    def has_cards(self, cards, cur_cards=None):
        if cur_cards is None:
            cur_cards = self.cards
        return len(set(cards) & set(cur_cards)) == len(set(cards))

    def get_cards(self, n, candidates):
        cards = []
        cur = []

        def dfs(k):
            if len(candidates) < n:
                return
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

    def play(self):
        res, to_all = {}, None
        self.gcore.check_pre_player(self.player.id)
        num = len(self.gcore.pre_cards.cards) if self.gcore.pre_cards else 0
        cards = self.valid_cards[num]
        print(str_cards_list(self.valid_cards[0]), num)
        for cs in cards:
            if not self.has_cards(cs.raw_cards):
                continue
            d = {'playCards': cs.raw_cards}
            res, to_all = self.server.post_cards(self.player.id, d)
            if res:
                self.pre_is_pass = False
                if 'winner' not in res:
                    for c in cs.raw_cards:
                        self.cards.remove(c)
                    self.valid_cards[0].remove(cs)
                if self.split_cards:
                    self.split_cards = False
                    self.valid_cards = self.get_valid_cards()
                break
        if not res:
            if self.pre_is_pass:
                self.continue_pass += 1
            self.pre_is_pass = True
            if self.continue_pass == 2:
                self.continue_pass = 0
                self.split_cards = True
                self.valid_cards = self.get_valid_cards()
            res, to_all = self.server.pass_turn(self.player.id)
        return res, to_all

    def send(self, data):
        if self.gcore.cur_player == self.player.id:
            self.server.delay(2)
            res, to_all = self.play()
            self.server.send_msg(res, to_all, self.player.processor)

    def ready(self):
        res, to_all = self.server.ready(self.player.id)
        self.set_cards()
        self.server.send_msg(res, to_all, self.player.processor)

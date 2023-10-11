import copy
import json
import time


class Computer(object):
    def __init__(self, player, server):
        self.player = player
        self.server = server
        self.gcore = server.gcore
        self.cards = self.gcore.get_cards(player.id)

    def set_cards(self):
        self.cards = self.gcore.get_cards(self.player.id)

    def get_cards(self, n):
        cards = []
        cur = []

        def dfs(k):
            if len(cur) == n:
                cards.append(copy.copy(cur))
            elif len(cur) < n:
                if k < len(self.cards):
                    cur.append(self.cards[k])
                    dfs(k + 1)
                    cur.pop()
                    dfs(k + 1)

        dfs(0)
        return cards

    def send(self, data):
        data = json.loads(data)
        print("computer " + str(self.player.id) + "view: ", data)
        if self.gcore.cur_player == self.player.id:
            time.sleep(2)
            res, to_all = {}, None
            self.gcore.check_pre_player(self.player.id)
            num = len(self.gcore.pre_cards.cards) if self.gcore.pre_cards else 0
            cards = []
            if num == 0:
                for i in range(5, 0, -1):
                    cards += self.get_cards(i)
            else:
                cards = self.get_cards(num)
            for cs in cards:
                d = {'playCards': cs}
                res, to_all = self.server.post_cards(self.player.id, d)
                if res:
                    print("computer " + str(self.player.id) + " play: ", res)
                    if 'winner' not in res:
                        for c in cs:
                            self.cards.remove(c)
                    break
            if not res:
                res, to_all = self.server.pass_turn(self.player.id)
                print("computer " + str(self.player.id) + " pass ...", res)
            self.server.send_msg(res, to_all, self.player.processor)

    def ready(self):
        res, to_all = self.server.ready(self.player.id)
        self.set_cards()
        self.server.send_msg(res, to_all, self.player.processor)

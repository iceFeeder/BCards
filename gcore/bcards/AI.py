import json


class Computer(object):
    def __init__(self, player, server):
        self.player = player
        self.server = server
        self.gcore = server.gcore
        self.cards = self.gcore.get_cards(player.id)

    def send(self, data):
        data = json.loads(data)
        print("computer view: ", data)
        res, to_all = {}, None
        if self.gcore.cur_player == self.player.id:
            pre = self.gcore.pre_cards
            if not pre or len(pre.cards) == 1:
                for c in self.cards:
                    d = {'playCards': [c]}
                    res, to_all = self.server.post_cards(self.player.id, d)
                    print("com play: ", res)
                    self.cards.remove(c)
                    if res:
                        break
            if not res:
                print("com pass ...")
                res, to_all = self.server.pass_turn(self.player.id)
            self.server.send_msg(res, to_all, self.player.location)

    def ready(self):
        return self.server.ready(self.player.id)

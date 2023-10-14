import abc

from gcore.bcards.bcards import BCards
import constant
from gcore.player import *
from gcore.bcards.AI import *
import json

GAME_MAP = {
    'BCards': BCards
}


class Server(object):
    def __new__(cls, ip, port, game, *args, **kwargs):
        obj = super(Server, cls).__new__(cls, *args, **kwargs)
        obj.route('/', 'GET', obj.index)
        obj.route('/player/<id>', 'GET', obj.deal)
        obj.route('/static/<filename>', 'GET', obj.load_static)
        obj.route('/static/faces/<img>', 'GET', obj.load_img)
        return obj

    def __init__(self, ip, port, game, *args, **kwargs):
        self.ip = ip
        self.port = port
        self.gcore = GAME_MAP[game]()
        self.players = []
        self.shuffle()

    def pre_check(self):
        return len(self.players) < self.gcore.max_players

    def notify(self):
        data = {"type": "init", "players": [p.covert2json() for p in self.players]}
        for i in range(len(self.players)):
            self.players[i].processor.send(json.dumps(data))

    def add_player(self, player_type, processor):
        if not self.pre_check():
            return None
        player_id = len(self.players)
        player_name = "Player" + str(player_id)
        player = Player(player_name, player_id, player_type, processor)
        self.players.append(player)
        print(player_name + "enter.")
        print("Players: ", self.players)
        return player

    def pass_turn(self, player_id, data=None):
        if not self.gcore.pass_player(player_id):
            return {}, None
        return {"type": "pass", 'cur_player_id': self.gcore.cur_player}, constant.TO_ALL

    def ready(self, player_id, data=None):
        res = {"type": "ready", "start": False}
        self.players[player_id].ready = 1
        if self.gcore.ready(player_id, self.players):
            res['start'] = True
            res['cur_player_id'] = self.gcore.cur_player
            res['player_cards'] = self.gcore.player_cards
            res['player_scores'] = self.gcore.player_scores
            response = {}
            for i in range(len(self.players)):
                response[i] = copy.copy(res)
                response[i]['cards'] = self.gcore.get_cards(i)
                response[i]['player_id'] = i
            return response, constant.DISPATCH
        res['players'] = [p.covert2json() for p in self.players]
        return res, constant.TO_ALL

    def get_cards(self, player_id, data=None):
        response = {'cards': self.gcore.get_cards(player_id),
                    'type': "init", 'player_id': player_id}
        return response, None

    def post_cards(self, player_id, data):
        if player_id != self.gcore.cur_player:
            return {}, None
        response = {'type': "play", 'player_id': player_id}
        play_cards = data['playCards']
        if self.gcore.check(play_cards, player_id):
            response['playCards'] = data['playCards']
            response['player_cards'] = self.gcore.player_cards
            self.gcore.update_player()
            response['cur_player_id'] = self.gcore.cur_player
            over = self.gcore.game_over()
            response['player_scores'] = self.gcore.player_scores
            if over >= 0:
                response['winner'] = over
                self.gcore.pre_winner = over
                self.gcore.reset()
                self.gcore.com_ready(self.players)
            return response, constant.TO_ALL
        return {}, None

    def add_com(self, player_id, data):
        player = self.add_player(PlayerType.Computer, None)
        if not player:
            return {}, None
        computer = Computer(player, self)
        player.set_processor(computer)
        computer.ready()
        return {}, None

    def shuffle(self):
        self.gcore.shuffle()

    def deal(self, id=0):
        ret, to_all = self.get_cards(id)
        return ret

    def reset(self):
        self.gcore.reset()

    @abc.abstractmethod
    def run(self):
        raise NotImplementedError

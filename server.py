import abc

from gcore.bcards.bcards import BCards
import random

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
        self.cur_player = None
        self.player_num = None
        self.ok = set()
        self.shuffle()

    def pre_check(self):
        return len(self.players) < self.gcore.max_players

    def pass_turn(self, player_id, data=None):
        if player_id != self.cur_player:
            return {}, False
        self.cur_player = (self.cur_player + 1) % self.player_num
        self.gcore.clear()
        return {"type": "pass", 'cur_player_id': self.cur_player}, True

    def ready(self, player_id, data=None):
        self.ok.add(player_id)
        response = {"type": "ready", "start": False}
        if len(self.ok) == len(self.players) and len(self.ok) != 1:
            response['start'] = True
            self.cur_player = random.randint(0, len(self.ok) - 1)
            self.player_num = len(self.ok)
            response['cur_player_id'] = self.cur_player
            return response, True
        return {}, False

    def get_cards(self, player_id, data=None):
        response = {'cards': self.gcore.get_cards(player_id),
                    'type': "init", 'player_id': player_id}
        return response, False

    def post_cards(self, player_id, data):
        if player_id != self.cur_player:
            return {'playCards': []}, False
        response = {'type': "play", 'player_id': player_id}
        play_cards = data['playCards']
        if self.gcore.check(play_cards):
            response['playCards'] = data['playCards']
            self.cur_player = (self.cur_player + 1) % self.player_num
            response['cur_player_id'] = self.cur_player
            return response, True
        return {}, False

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

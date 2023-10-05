import json
import abc

from gcore.bcards.bcards import BCards
import constant

GAME_MAP = {
    'BCards': BCards
}


class Server(object):
    ACTIONS = {
        'get': 'get_cards',
        'put': 'ready',
        'post': 'post_cards',
    }

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
        self.ok = set()
        self.shuffle()

    def pre_check(self):
        return len(self.players) < self.gcore.max_players

    def ready(self, player_id, data=None):
        self.ok.add(player_id)
        response = {"type": "ready", "start": False}
        if len(self.ok) == len(self.players) and len(self.ok) != 1:
            response['start'] = True
            return json.dumps(response), True
        return json.dumps(response), False

    def get_cards(self, player_id, data=None):
        response = {'cards': self.gcore.get_cards(player_id),
                    'type': "init", 'player_id': player_id}
        return json.dumps(response), False

    def post_cards(self, player_id, data):
        response = {'type': "play", 'player_id': player_id}
        play_cards = data['playCards']
        if self.gcore.check(play_cards):
            response['playCards'] = data['playCards']
            return json.dumps(response), True
        response['playCards'] = []
        return json.dumps(response), False

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

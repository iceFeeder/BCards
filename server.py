import abc

from gcore.bcards.bcards import BCards
import constant
import copy

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

    def pass_turn(self, player_id, data=None):
        if not self.gcore.pass_player(player_id):
            return {}, None
        return {"type": "pass", 'cur_player_id': self.gcore.cur_player}, constant.TO_ALL

    def ready(self, player_id, data=None):
        res = {"type": "ready", "start": False}
        if self.gcore.ready(player_id, self.players):
            res['start'] = True
            res['cur_player_id'] = self.gcore.cur_player
            res['player_cards'] = self.gcore.player_cards
            response = {}
            for i in range(len(self.players)):
                response[i] = copy.copy(res)
                response[i]['cards'] = self.gcore.get_cards(i)
                response[i]['player_id'] = i
            return response, constant.DISPATCH
        return {}, None

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
            if over >= 0:
                response['winner'] = over
                self.gcore.reset()
            return response, constant.TO_ALL
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

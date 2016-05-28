import json
import abc
from bcards import BCards
import constant

GAME_MAP = {
    'BCards':BCards
}

class Server(object):
    ACTIONS = {
        'get':'get_cards',
        'put':'show_cards',
    }

    def __new__(cls, *args, **kwargs):
        obj = super(Server, cls).__new__(cls, *args, **kwargs)
        obj.route('/','GET',obj.index)
        obj.route('/player/<id>','GET',obj.deal)
        return obj

    def __init__(self,ip,port,game):
        self.ip = ip
        self.port = port
        self.gcore = GAME_MAP[game]()
        self.players = set()
        self.shuffle()

    def show_cards(self,cards):
        import pdb;pdb.set_trace()
        if self.gcore.check(cards):
            return json.dumps(cards), True
        else:
            return constant.CHECK_FAIL, False

    def get_cards(self, index):
        response = {}
        response['cards'] = self.gcore.get_cards(index)
        return json.dumps(response), False

    def shuffle(self):
        self.gcore.shuffle()

    def deal(self,id = 0):
        ret, to_all = self.get_cards(id)
        return ret

    @abc.abstractmethod
    def run(self):
        raise NotImplementedError

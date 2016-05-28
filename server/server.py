import json
import abc
from cardspool import CardsPool

class Server(object):

    ACTIONS = {
        'get':'get_cards',
        'put':'',
    }

    def __new__(cls, *args, **kwargs):
        obj = super(Server, cls).__new__(cls, *args, **kwargs)
        obj.route('/','GET',obj.index)
        obj.route('/<id>','GET',obj.deal)
        return obj

    def __init__(self,ip,port):
        self.ip = ip
        self.port = port
        self.pool = CardsPool()
        self.players = set()
        self.shuffle()

    def get_cards(self, index):
        response = {}
        response['cards'] = self.pool.get_cards(index)
        return json.dumps(response), False
        
    def shuffle(self):
        self.pool.shuffle()

    def deal(self,id = 0):
        ret , to_all = self.get_cards(id)
        return ret

    @abc.abstractmethod
    def run(self):
        raise NotImplementedError

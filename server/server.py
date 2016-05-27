import json
import abc
from cardspool import CardsPool

class Server(object):

    ACTIONS = {
        'get':'get_cards'
    }

    players = set()
    pool = CardsPool()

    def __init__(self,ip,port):
        self.ip = ip
        self.port = port
        self.shuffle()

    @classmethod
    def get_cards(cls, index):
        response = {}
        response['cards'] = cls.pool.get_cards(index)
        return json.dumps(response),False
        
    def shuffle(self):
        self.pool.shuffle()

    @abc.abstractmethod
    def run(self):
        raise NotImplementedError

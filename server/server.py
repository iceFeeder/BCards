import json
import abc
from cardspool import POOL as pool

pool.shuffle()

class Server(object):

    @classmethod
    def get_cards(cls, index):
        response = {}
        response['cards'] = pool.get_cards(index) 
        return json.dumps(response)
        
    @abc.abstractmethod
    def run(self):
        pass

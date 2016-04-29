from server import Server
from bottle import route , run


class BottleServer(Server):

    @route('/index/:id')
    def deal(id = 0):
        return Server.get_cards(id)

    def run(self):
        run(host=self.ip,port=self.port)


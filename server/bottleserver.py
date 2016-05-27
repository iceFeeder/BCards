from server import Server
from bottle import default_app, get, template, run, route
from bottle.ext.websocket import GeventWebSocketServer
from bottle.ext.websocket import websocket
import json

class BottleServer(Server):

    @get('/')
    def index():
        return template('index')

    @get('/websocket', apply=[websocket])
    def connection(ws):
        Server.players.add(ws)
        while True:
            msg = ws.receive()
            if msg is not None:
                msg = json.loads(msg)
                if msg['action'] in Server.ACTIONS:
                    method = getattr(Server,Server.ACTIONS[msg['action']])
                    ret, to_all = method(msg['data'])
                    if to_all:
                        for p in Server.players:
                            p.send(ret)
                    else:
                        ws.send(ret)
            else: break
        Server.players.remove(ws)

    @route('/index/:id')
    def deal(id = 0):
        return Server.get_cards(id)

    def run(self):
        run(host=self.ip,port=self.port,server=GeventWebSocketServer)


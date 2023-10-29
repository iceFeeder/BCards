import time

from gcore.bcards.AI import Computer
from server import Server
import bottle
from bottle.ext.websocket import GeventWebSocketServer, websocket
import json
import constant
from gcore.player import Player, PlayerType
import traceback


@bottle.error(400)
def error_400(err):
    return err.body


@bottle.error(403)
def error_403(err):
    return err.body


@bottle.error(404)
def error_404(err):
    return err.body


@bottle.error(409)
def error_409(err):
    return err.body


@bottle.error(500)
def error_500(err):
    return err.body


@bottle.error(503)
def error_503(err):
    return err.body


class BottleServer(Server):
    def __new__(cls, *args, **kwargs):
        obj = super(BottleServer, cls).__new__(cls, *args, **kwargs)
        obj.route('/websocket', 'GET', obj.connection, apply=[websocket])
        return obj

    def index(self):
        return bottle.template('./ui/index')

    def load_static(self, filename):
        return bottle.static_file(filename, root='./ui/')

    def load_img(self, img):
        return bottle.static_file(img, root='./ui/faces/')

    def delay(self, sec):
        self.event_queue.append((None, sec))

    def send_msg(self, response, to_all, processor):
        if response:
            if to_all:
                for i in range(len(self.players)):
                    if to_all == constant.TO_ALL:
                        self.event_queue.append((self.players[i].processor, json.dumps(response)))
                    elif to_all == constant.DISPATCH:
                        self.event_queue.append((self.players[i].processor, json.dumps(response[i])))
            else:
                self.event_queue.append(processor, json.dumps(response))
            while self.event_queue:
                p, data = self.event_queue.pop(0)
                if p:
                    p.send(data)
                else:
                    time.sleep(data)

    def connection(self, ws):
        player = self.add_player(PlayerType.Human, ws)
        if not player:
            return
        self.notify()
        while True:
            try:
                msg = ws.receive()
                if msg is not None:
                    msg = json.loads(msg)
                    method = getattr(self, msg['action'])
                    player_id = self.players.index(player)
                    ret, to_all = method(player_id, msg['data'])
                    self.send_msg(ret, to_all, ws)
                else:
                    break
            except Exception as e:
                print("got Exception: ", str(e))
                traceback.print_stack()
                break
        print("Game Over...")
        print(player.name + " quit.")
        self.reset(player)
        self.gcore.reset_scores()
        self.notify()

    def route(self, uri, method, handler, apply=None):
        def handler_trap_exception(*args, **kwargs):
            try:
                response = handler(*args, **kwargs)
                return response
            except Exception as e:
                raise

        bottle.route(uri, method, handler_trap_exception, apply=apply)

    def run(self):
        bottle.run(host=self.ip, port=self.port, server=GeventWebSocketServer)

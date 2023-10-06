from server import Server
import bottle
from bottle.ext.websocket import GeventWebSocketServer, websocket
import json


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

    def connection(self, ws):
        if not self.pre_check():
            return
        self.players.append(ws)
        print("players: ", self.players)
        while True:
            try:
                msg = ws.receive()
                if msg is not None:
                    msg = json.loads(msg)
                    print(msg)
                    method = getattr(self, msg['action'])
                    player_id = self.players.index(ws)
                    ret, to_all = method(player_id, msg['data'])
                    print("ret: ", ret)
                    if ret:
                        if to_all:
                            for p in self.players:
                                p.send(json.dumps(ret))
                        else:
                            ws.send(json.dumps(ret))
                else:
                    break
            except Exception as e:
                print("got Exception: ", str(e))
                break
        print("Game Over...")
        self.reset()
        self.players.clear()

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
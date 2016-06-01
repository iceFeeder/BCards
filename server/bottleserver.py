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
        obj.route('/websocket','GET',obj.connection,apply=[websocket])
        return obj

    def index(self):
        return bottle.template('./example/index')

    def load_static(self,filename):
        return bottle.static_file(filename, root='./example/')

    def load_img(self,img):
        return bottle.static_file(img, root='./example/faces/')

    def connection(self,ws):
        self.players.add(ws)
        while True:
            msg = ws.receive()
            if msg is not None:
                try:
                    msg = json.loads(msg)
                except Exception as e:
                    print e.message
                    break
                if msg['action'] in self.ACTIONS:
                    method = getattr(self,self.ACTIONS[msg['action']])
                    ret, to_all = method(msg['data'])
                    if to_all:
                        for p in self.players:
                            p.send(ret)
                    else:
                        ws.send(ret)
            else: break
        self.players.remove(ws)

    def route(self, uri, method, handler,apply = None):
        def handler_trap_exception(*args, **kwargs):
            try:
                response = handler(*args, **kwargs)
                return response
            except Exception as e:
                raise
        bottle.route(uri, method, handler_trap_exception, apply=apply)

    def run(self):
        bottle.run(host=self.ip,port=self.port,server=GeventWebSocketServer)


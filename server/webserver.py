import web
from server import Server
import sys

urls = (
    '/index/(.*)', 'WebServer'
)

class WebServer(Server):

    def GET(self,index):
        return Server.get_cards(index)

    def run(self):
        sys.argv[1:] = [self.ip+":"+str(self.port)]
        app = web.application(urls,{'WebServer': WebServer})
        app.run()


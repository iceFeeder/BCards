import web
from server import Server

urls = (
    '/index/(.*)', 'WebServer'
)

class WebServer(Server):
    def GET(self,index):
        return Server.get_cards(index)

    def run(self):
        app = web.application(urls,{'WebServer': WebServer})
        app.run()


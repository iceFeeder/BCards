import web
import cardspool as pool

render = web.template.render('templates/')

urls = (
    '/index=(.*)', 'Server'
)

cards = pool.CardsPool()
cards.shuffle()

class Server:
    def GET(self,index):
        return cards.get_cards(index)

if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()

import web
import cardspool as pool
import json

render = web.template.render('templates/')

urls = (
    '/index/(.*)', 'Deal'
)

cards = pool.CardsPool()
cards.shuffle()

class Deal:
    def GET(self,index):
        response = {}
        response['cards'] = cards.get_cards(index)
        return json.dumps(response)

if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()

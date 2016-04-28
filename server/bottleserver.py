from bottle import route , run
import json
import cardspool as pool

cards = pool.CardsPool()
cards.shuffle()

@route('/index/:id')
def deal(id = 0):
    response = {}
    response['cards'] = cards.get_cards(id)
    return json.dumps(response)

run(host="0.0.0.0",port=8080)



from cardspool import CardsPool

class BCards(CardsPool):
    def __init__(self):
        super(BCards,self).__init__(size=52)
    def check(self,data):
        print data
        return True

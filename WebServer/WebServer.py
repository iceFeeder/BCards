import web
import 

render = web.template.render('templates/')

urls = (
    '/(.*)', 'Server'
)

class Server:
    cards = CardsPool()
    def GET(self,name):
        return render.my_template(name)

if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()

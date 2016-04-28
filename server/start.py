from config import CNF
from bottleserver import BottleServer
from webserver import WebServer

SERVER_MAP = {
    "bottle": BottleServer,
    "web": WebServer,
}

if __name__ == "__main__":
    if CNF.args.framework in SERVER_MAP:
        server = SERVER_MAP[CNF.args.framework]()
        server.run()
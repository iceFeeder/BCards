#!/usr/env python
''' Python script to start a web server for BCard .'''

from bottleserver import BottleServer
from webserver import WebServer
from ConfigParser import SafeConfigParser
import argparse
import os
import sys
import textwrap

SCRIPTDIR = os.path.abspath(os.path.dirname(sys.argv[0]))

SERVER_MAP = {
    "bottle": BottleServer,
    "web": WebServer,
}

class Parser:
    def __init__(self, desc, args=[]):
        self.unparsed_args = args
        self.cfg_file = None
        self.parser = None
        desc               = textwrap.fill(textwrap.dedent(desc).strip(), width=79)
        self.desc          = 'Description:\n%s\n%s\n\n' %(desc, '-' * 79)
        self.define_args()
        self.args = self.load_config_file()

    def define_args(self):
        cparser = argparse.ArgumentParser(add_help=False)
        cparser.add_argument('--config', '-c',
                             action='store',
                             default=os.path.join(SCRIPTDIR, 'config.cfg'),
                             help='Config File for the Server')
        file_ns, rargs = cparser.parse_known_args(self.unparsed_args)
        self.cfg_file = file_ns.config

        aparser = argparse.ArgumentParser(parents=[cparser],
                                          formatter_class=argparse.RawTextHelpFormatter,
                                          description=self.desc)
        aparser.add_argument('--framework','-f',
                             action='store',
                             default='bottle',
                             help='web server framework')
        aparser.add_argument('--listen_ip','-i',
                             action='store',
                             default='0.0.0.0',
                             help='listening ip address')
        aparser.add_argument('--port','-p',
                             action='store',
                             default='8080',
                             help='listening port')

        aparser.parse_args(self.unparsed_args)
        self.parser = aparser

    def load_config_file(self):
        config = SafeConfigParser()
        config.read(self.cfg_file)
        for section in config.sections():
             self.parser.set_defaults(**dict(config.items(section)))
        return self.parser.parse_args(self.unparsed_args)


if __name__ == "__main__":
    parser = Parser(__doc__, sys.argv[1:])
    if parser.args.framework in SERVER_MAP:
        server = SERVER_MAP[parser.args.framework](parser.args.listen_ip, parser.args.port)
        server.run()

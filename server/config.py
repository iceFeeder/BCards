from ConfigParser import ConfigParser
import argparse

CONF_FILE = "./server.conf"

class Config:
    def __init__(self, config_file):
        self.args = self._load_config(config_file)

    def _load_config(self, config_file):
        config = ConfigParser()
        config.read(config_file)
        conf_parser = argparse.ArgumentParser()
        for section in config.sections():
             conf_parser.set_defaults(**dict(config.items(section)))
        return conf_parser.parse_args()

CNF = Config(CONF_FILE)


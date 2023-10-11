from enum import IntEnum


class PlayerType(IntEnum):
    Human = 0
    Computer = 1


class Player(object):
    def __init__(self, name, player_id, player_type, processor):
        self.name = name
        self.id = player_id
        self.type = player_type
        self.processor = processor
        self.ready = 0

    def set_processor(self, processor):
        self.processor = processor

    def covert2json(self):
        return {"name": self.name, "ready": self.ready}

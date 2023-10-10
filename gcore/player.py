from enum import IntEnum


class PlayerType(IntEnum):
    Human = 0
    Computer = 1


class Player(object):
    def __init__(self, name, player_id, player_type, location):
        self.name = name
        self.id = player_id
        self.type = player_type
        self.location = location
        self.ready = 0

    def set_location(self, location):
        self.location = location

    def covert2json(self):
        return {"name": self.name, "ready": self.ready}

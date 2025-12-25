import json
import os


class GameData:
    def __init__(self, data_dir):
        self.rooms = self.load_json(os.path.join(data_dir, "rooms.json"))
        self.objects = self.load_json(os.path.join(data_dir, "objects.json"))
        self.bools = self.load_json(os.path.join(data_dir, "bools.json"))
        self.inputs = self.load_json(os.path.join(data_dir, "inputs.json"))
        self.media = self.load_json(os.path.join(data_dir, "media.json"))
        self.config = self.load_json(os.path.join(data_dir, "game.json"))
        self.messages = self.load_json(os.path.join(data_dir, "messages.json"))

        self.start_room = self.config["start_room"]

    def load_json(self, path):
        with open(path, "r", encoding="utf8") as f:
            return json.load(f)

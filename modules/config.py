import json
from pathlib import Path

class Config():
    def __init__(self):
        # path to config file
        self.path = Path('config.json')

        # default configuration
        self.base = {
            "material_id": {
                "air": 0,
                "wood": 1,
                "leaf": 2,
                "wall": 3
            },
            "material_color": {
                "wood": [139, 69, 19],
                "leaf": [0, 128, 0],
                "wall": [0, 0, 0]
            },
            "material_translucency": {
                "air": 100,
                "wood": 0,
                "leaf": 50,
                "wall": 0
            }
        }

        # holds config loaded from file
        self.config = {}

        # create config file with default values, if it does not exist
        if not self.path.is_file():
            self.create_file()

    
    def create_file(self):
        """create config file if it not already exists"""
        with open(self.path, 'w', encoding='UTF-8') as f:
            json.dump(self.base, f)

    def load(self):
        """load config dictionary from file"""
        with open(self.path, 'r', encoding='UTF-8') as f:
            self.config = json.load(f)
    
    def save(self):
        """save config dictionary to file"""
        with open(self.path, 'w', encoding='UTF-8') as f:
            json.dump(self.config, f)


    def get_material_id(self) ->  dict[str, int]:
        """return the material ids from the config"""
        self.load()
        return self.config['material_id']

    def get_material_color(self) -> dict[str, list[int]]:
        """return the material colors from the config"""
        self.load()
        return self.config['material_color']

    def get_material_translucency(self) -> dict[str, int]:
        """return the material translucency in percent from the config"""
        self.load()
        return self.config['material_translucency']
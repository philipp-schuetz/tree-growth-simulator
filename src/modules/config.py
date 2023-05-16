"""holds the default configuration and methods to interact with the config file"""
import json
from pathlib import Path

class Config():
    def __init__(self) -> None:
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
            },
            "model_dimensions": {
                "width": 249,
                "height": 498
            },
            "l_system": {
                "iterations": 1,
                "radius": 16,
                "axiom": "C",
                "rules": [
                    {"letter": "C", "new_letters": "CPrCPrCPrCPrCPrCPrCPrCPr"},
                ]
            },
            "image_generation": {
                "add_leafs": True
            },
            "light": {
                "minimum": 20
            }
        }

        # holds config loaded from file
        self.config = {}

        # create config file with default values, if it does not exist
        self.create_file()

    def create_file(self):
        """create config file if it not already exists"""
        if not self.path.is_file():
            with open(self.path, 'w', encoding='UTF-8') as file:
                json.dump(self.base, file)

    def load(self):
        """load config dictionary from file"""
        with open(self.path, 'r', encoding='UTF-8') as file:
            self.config = json.load(file)

    def save(self):
        """save config dictionary to file"""
        with open(self.path, 'w', encoding='UTF-8') as file:
            json.dump(self.config, file)


    def get_material_id(self) ->  dict[str, int]:
        """return the material ids from the config"""
        self.load()
        # data validation
        for value in self.config['material_id'].values():
            if not isinstance(value, int):
                raise ValueError('material id must be an integer')
            elif value < 0:
                raise ValueError('material id must be greater than 0')
        return self.config['material_id']

    def get_material_color(self) -> dict[str, list[int]]:
        """return the material colors from the config"""
        self.load()
            # data validation
        for value in self.config['material_color'].values():
            if len(value) < 3 or len(value) > 3:
                raise ValueError('material color must be rgb values (r,g,b)')
            for color_value in value:
                if color_value < 0 or color_value > 255:
                    raise ValueError('material color must be rgb values (0<=rgb<=255)')
        return self.config['material_color']

    def get_material_translucency(self) -> dict[str, int]:
        """return the material translucency in percent from the config"""
        self.load()
        # data validation
        for value in self.config['material_translucency'].values():
            if not isinstance(value, int):
                raise ValueError('material translucency value must be an integer')
            elif value < 0 or value > 100:
                raise ValueError('material translucency value must be between 0 and 100')

        return self.config['material_translucency']

    def get_model_dimensions(self) -> dict[str, int]:
        """return model dimensions (width, height)"""
        self.load()

        width = self.config['model_dimensions']['width']
        height = self.config['model_dimensions']['height']
        # data validation
        if not isinstance(width, int) or not isinstance(height, int):
            raise ValueError('model width and height must be an integer')
        elif width*2 != height:
            raise ValueError('model width and height must have a 1:2 ratio')
        elif width <= 0 or height <= 0:
            raise ValueError('model width and height must be greater than 0')
        else:
            return self.config['model_dimensions']

    def get_minimum_light_level(self) -> int:
        """return the minimum light level needed to spawn wood or leafs"""
        self.load()

        minimum = self.config['light']['minimum']
        # data validation
        if not isinstance(minimum, int):
            raise ValueError('minimum light level must be an integer')
        elif minimum <= 0:
            raise ValueError('minimum light level must be positive')
        else:
            return minimum

    def get_iterations(self) -> int:
        """return l-system iteration count"""
        self.load()
        iterations = self.config['l_system']['iterations']

        # data validation
        if not isinstance(iterations, int):
            raise ValueError('iterations must be an integer')
        elif iterations < 1:
            raise ValueError('iterations must be at least 1')
        else:
            return iterations
    
    def get_radius(self) -> int:
        self.load()
        radius = self.config['l_system']['radius']
        # data validation
        if not isinstance(radius, int):
            raise ValueError('radius must be an integer')
        elif radius < 0:
            raise ValueError('radius must be positive')
        else:
            return radius

    def get_axiom(self) -> str:
        """return start letter for l-system"""
        self.load()
        start = self.config['l_system']['start']

        # data validation
        if not isinstance(start, str):
            raise ValueError('start must be a string')
        else:
            return start
        
    def get_rules(self) -> list[dict[str,str]]:
        """return rules for l-system"""
        self.load()
        rules = self.config['l_system']['rules']

        # data validation
        for rule in rules:
            if not isinstance(rule['letter'], str):
                raise ValueError('letter must be a string')
            elif len(rule['letter']) > 1:
                raise ValueError('letter must be a single character')
            elif not isinstance(rule['new_letters'], str):
                raise ValueError('new_letters must be a string')
        return rules
    
    def get_add_leafs(self) -> bool:
        """return True if image generation should use leafs, else return False"""
        self.load()
        boolean = self.config['image_generation']['add_leafs']

        # data validation
        if not isinstance(boolean, bool):
            raise ValueError('add_leafes value must be a boolean')
        return boolean

config = Config()
# print(get_model_dimensions())
# print(get_rules())
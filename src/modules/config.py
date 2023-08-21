"""holds the default configuration and methods to interact with the config file"""
import json
from pathlib import Path
import logging

class Config():
    """Config holds default contents for config.json and methods to apply the config"""
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
            "visualization": {
                "add_leafs": True
            },
            "material_colors": {
                "leaf": "green",
                "wood": "brown"
            },
            "light": {
                "minimum": 20
            },
            "water": {
                "minimum": 20
            },
            "temperature": {
                "minimum": 20
            },
            "nutrients": {
                "minimum": 20
            },
            "logging": True,
            "plot_filename": "plot",
            "random_seed": False,
            "save_array": False
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
        logging.info('created config file')

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
                logging.error('config: material id must be an integer')
                raise ValueError('material id must be an integer')
            if value < 0:
                logging.error('config: material id must be greater than 0')
                raise ValueError('material id must be greater than 0')
        return self.config['material_id']

    def get_material_translucency(self) -> dict[str, int]:
        """return the material translucency in percent from the config"""
        self.load()
        # data validation
        for value in self.config['material_translucency'].values():
            if not isinstance(value, int):
                logging.error('config: material translucency value must be an integer')
                raise ValueError('material translucency value must be an integer')
            if value < 0 or value > 100:
                logging.error('config: material translucency value must be between 0 and 100')
                raise ValueError('material translucency value must be between 0 and 100')

        return self.config['material_translucency']

    def get_model_dimensions(self) -> dict[str, int]:
        """return model dimensions (width, height)"""
        self.load()

        width = self.config['model_dimensions']['width']
        height = self.config['model_dimensions']['height']
        # data validation
        if not isinstance(width, int) or not isinstance(height, int):
            logging.error('config: model width and height must be an integer')
            raise ValueError('model width and height must be an integer')
        if width*2 != height:
            logging.error('config: model width and height must have a 1:2 ratio')
            raise ValueError('model width and height must have a 1:2 ratio')
        if width <= 0 or height <= 0:
            logging.error('config: model width and height must be greater than 0')
            raise ValueError('model width and height must be greater than 0')
        return self.config['model_dimensions']

    def get_minimum_values(self) -> list[int]:
        """return the minimum values of all modifiers for the tree to grow"""
        self.load()

        minimum_values = [
            self.config['light']['minimum'],
            self.config['water']['minimum'],
            self.config['temperature']['minimum'],
            self.config['nutrients']['minimum']
        ]
        for minimum in minimum_values:
            # data validation
            if not isinstance(minimum, int):
                logging.error('config: minimum values need to be an integer')
                raise ValueError('minimum values need to be an integer')
            if minimum <= 0:
                logging.error('config: minimum values need to be be positive')
                raise ValueError('minimum values need to be be positive')

        return minimum_values

    def get_add_leafs(self) -> bool:
        """return True if model should use leafs, else return False"""
        self.load()
        boolean = self.config['visualization']['add_leafs']

        # data validation
        if not isinstance(boolean, bool):
            logging.error('config: add_leafes value must be a boolean')
            raise ValueError('add_leafes value must be a boolean')
        return boolean

    def get_logging_enabled(self) -> bool:
        """return True if logging is enabled in config, else return False"""
        self.load()
        boolean = self.config['logging']

        # data validation
        if not isinstance(boolean, bool):
            logging.error('config: logging value must be a boolean')
            raise ValueError('logging value must be a boolean')
        return boolean

    def get_material_colors(self) ->  dict[str, str]:
        """return the material colors from the config"""
        self.load()
        # data validation
        for value in self.config['material_colors'].values():
            if not isinstance(value, str):
                logging.error('config: material color must be a string')
                raise ValueError('material color must be a string')
        return self.config['material_colors']

    def get_plot_filename(self) -> str:
        """return the filename for the plots generated by mathplotlib"""
        self.load()
        string = self.config['plot_filename']

        # data validation
        if not isinstance(string, str):
            logging.error('config: plot filename must be a string')
            raise ValueError('plot filename must be a string')
        return string

    def get_random_seed(self) -> int | bool:
        """return the seed for random number generation"""
        self.load()
        seed = self.config['random_seed']

        # data validation
        if isinstance(seed, int) or isinstance(seed, bool):
            return seed
        else:
            logging.error('config: random seed must be of type int or bool')
            raise ValueError('config: random seed must be of type int or bool')

    def get_save_array_enabled(self) -> bool:
        """return True if array saving is enabled in config, else return False"""
        self.load()
        boolean = self.config['save_array']

        # data validation
        if not isinstance(boolean, bool):
            logging.error('config: save_array value must be a boolean')
            raise ValueError('save_array value must be a boolean')
        return boolean

config = Config()

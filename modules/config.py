"""holds the default configuration and methods to interact with the config file"""
import json
from pathlib import Path

# path to config file
path = Path('config.json')

# default configuration
base = {
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
        "width": 250,
        "height": 500
    },
    "l_system": {
        "iterations": 4,
        "start": "X",
        "angle": 25,
        "rules": [
            {"letter": "X", "new_letters": "F+[[X]-X]-F[-FX]+X"},
            {"letter": "F", "new_letters": "FF"}
        ]
    }
}

# holds config loaded from file
config = {}

def create_file():
    """create config file if it not already exists"""
    with open(path, 'w', encoding='UTF-8') as file:
        json.dump(base, file)

def load():
    """load config dictionary from file"""
    with open(path, 'r', encoding='UTF-8') as file:
        config = json.load(file)

def save():
    """save config dictionary to file"""
    with open(path, 'w', encoding='UTF-8') as file:
        json.dump(config, file)


def get_material_id() ->  dict[str, int]:
    """return the material ids from the config"""
    load()
    # data validation
    for value in config['material_id'].values():
        if not isinstance(value, int):
            raise ValueError('material id must be an integer')
        elif value < 0:
            raise ValueError('material id must be greater than 0')
    return config['material_id']

def get_material_color() -> dict[str, list[int]]:
    """return the material colors from the config"""
    load()
        # data validation
    for value in config['material_color'].values():
        if len(value) < 3 or len(value) > 3:
            raise ValueError('material color must be rgb values (r,g,b)')
        for color_value in value:
            if color_value < 0 or color_value > 255:
                raise ValueError('material color must be rgb values (0<=rgb<=255)')
    return config['material_color']

def get_material_translucency() -> dict[str, int]:
    """return the material translucency in percent from the config"""
    load()
    # data validation
    for value in config['material_translucency'].values():
        if not isinstance(value, int):
            raise ValueError('material translucency value must be an integer')
        elif value < 0 or value > 100:
            raise ValueError('material translucency value must be between 0 and 100')

    return config['material_translucency']

def get_model_dimensions() -> dict[str, int]:
    """return model dimensions (width, height)"""
    load()

    width = config['model_dimensions']['width']
    height = config['model_dimensions']['height']
    # data validation
    if not isinstance(width, int) or not isinstance(height, int):
        raise ValueError('model width and height must be an integer')
    elif width*2 != height:
        raise ValueError('model width and height must have a 1:2 ratio')
    elif width <= 0 or height <= 0:
        raise ValueError('model width and height must be greater than 0')
    else:
        return config['model_dimensions']

def init_config():
    # create config file with default values, if it does not exist
    if not path.is_file():
        create_file()
import numpy as np
import modules.config as config
# TODO: finish light calculation

class Light:
    def __init__(self):
        self.config = config.Config()
        # {0: 100, 1: 0, 2: 50, 3: 0}
        self.translucency = {}
        self.set_translucency()

        # create variable for light model dimensions and set them with config
        self.width = 0
        self.height = 0
        self.set_dimensions()

        self.lightarray = np.zeros((self.width, self.height, self.width))

        # get light value from ui

    def set_translucency(self):
        ids = self.config.get_material_id()
        translucency = self.config.get_material_translucency()
        for id in ids.keys():
            self.translucency[ids[id]] = translucency[id]
        print(self.translucency)

    def set_dimensions(self):
        'fetch and set model dimensions from config file'
        dimensions = self.config.get_model_dimensions()
        self.width = dimensions['width']
        self.height = dimensions['height']

    def calculate(self, baselight:int):
        """calculates the lightvalue for each voxel"""
        return

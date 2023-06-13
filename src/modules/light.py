import numpy as np
from modules.config import config

class Light:
    def __init__(self):
        # {0: 100, 1: 0, 2: 50, 3: 0}
        self.translucency = {}
        self.set_translucency()

        # create variable for light model dimensions and set them with config
        self.width = -1
        self.height = -1
        self.set_dimensions()

        self.lightarray = np.zeros((self.width, self.height, self.width))

        self.lightlevel = -1

        self.activated_sides = ['front','back','left','right','top']

    def set_translucency(self):
        """combine material ids and material translucency from config file
        into translucency dictionary"""
        ids = config.get_material_id()
        translucency = config.get_material_translucency()
        for id in ids.keys():
            self.translucency[ids[id]] = translucency[id]

    def set_dimensions(self):
        """fetch and set model dimensions from config file"""
        dimensions = config.get_model_dimensions()
        self.width = dimensions['width']
        self.height = dimensions['height']

    def set_light(self, light):
        """set inital lightlevel from ui"""
        self.lightlevel = light

    def calculate(self, model):
        """calculates the lightvalue for each voxel \n
        only one lightvalue is calculated per voxel\n
        the value calculated refers to the side most close to the models edge"""

        for side in self.activated_sides:
            if side == 'front':
                # iterate through map and add visible voxels to array
                for layer in range(0, self.width):
                    for row in range(0, self.height):
                        for voxel in range(0, self.width):
                            # set outer layer of voxels to initital light level
                            if layer == 0:
                                self.lightarray[layer,row,voxel] = self.lightlevel
                            else:
                                # calculate new light value and add it to light array
                                light_back = self.lightarray[layer-1,row,voxel]
                                translucency_back = self.translucency[model[layer-1,row,voxel]]
                                self.lightarray[layer,row,voxel] += light_back*(translucency_back/100)

            elif side == 'back':
                # iterate through map and add visible voxels to array
                for layer in range(self.width-1,-1,-1):
                    for row in range(0, self.height):
                        for voxel in range(0, self.width):
                            # set outer layer of voxels to initital light level
                            if layer == self.width-1:
                                self.lightarray[layer,row,voxel] = self.lightlevel
                            else:
                                # calculate new light value and add it to light array
                                light_back = self.lightarray[layer+1,row,voxel]
                                translucency_back = self.translucency[model[layer+1,row,voxel]]
                                self.lightarray[layer,row,voxel] += light_back*(translucency_back/100)

            elif side == 'left':
                for layer in range(0, self.width):
                    for row in range(0, self.height):
                        for voxel in range(0, self.width):
                            # set outer layer of voxels to initital light level
                            if voxel == 0:
                                self.lightarray[layer,row,voxel] = self.lightlevel
                            else:
                                # calculate new light value and add it to light array
                                light_back = self.lightarray[layer,row,voxel-1]
                                translucency_back = self.translucency[model[layer,row,voxel-1]]
                                self.lightarray[layer,row,voxel] += light_back*(translucency_back/100)

            elif side == 'right':
                for layer in range(0, self.width):
                    for row in range(0, self.height):
                        for voxel in range(self.width-1,-1,-1):
                            # set outer layer of voxels to initital light level
                            if voxel == self.width-1:
                                self.lightarray[layer,row,voxel] = self.lightlevel
                            else:
                                # calculate new light value and add it to light array
                                light_back = self.lightarray[layer,row,voxel+1]
                                translucency_back = self.translucency[model[layer,row,voxel+1]]
                                self.lightarray[layer,row,voxel] += light_back*(translucency_back/100)

            elif side == 'top':
                for layer in range(0, self.width):
                    for row in range(0, self.height):
                        for voxel in range(0, self.width):
                            # set outer layer of voxels to initital light level
                            if row == 0:
                                self.lightarray[layer,row,voxel] = self.lightlevel
                            else:
                                # calculate new light value and add it to light array
                                light_back = self.lightarray[layer,row-1,voxel]
                                translucency_back = self.translucency[model[layer,row-1,voxel]]
                                self.lightarray[layer,row,voxel] += light_back*(translucency_back/100)
                                
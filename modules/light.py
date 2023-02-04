import numpy as np
import modules.config as config
# TODO: finish light calculation

class Light:
    def __init__(self, model):
        self.config = config.Config()
        # {0: 100, 1: 0, 2: 50, 3: 0}
        self.translucency = {}
        self.set_translucency()

        # create variable for light model dimensions and set them with config
        self.width = -1
        self.height = -1
        self.set_dimensions()

        self.lightarray = np.zeros((self.width, self.height, self.width))

        self.lightlevel = -1

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

    def set_light(self, light):
        """set inital lightlevel from ui"""
        self.lightlevel = light

    def calculate(self, model):
        """calculates the lightvalue for each voxel \n
        only one lightvalue is calculated per voxel\n
        the value calculated refers to the side most close to the models edge"""

        # sides = ['front','back','left','right','top']
        sides = {'front':100,'back':100,'left':100,'right':100,'top':100}

        for side in sides:
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

            if side == 'back':
                # iterate through map and add visible voxels to array
                for layer in range(self.width-1,-1,-1):
                    for row in range(0, self.height):
                        for voxel in range(0, self.width):
                            # set outer layer of voxels to initital light level
                            if layer == self.width-1:
                                self.lightarray[layer,row,voxel] = self.lightlevel
                            # get light value of last voxel, reduce it and add to lightarray
                            self.lightarray[layer,row,voxel]

            if side == 'left': # calculation correct?
                for layer in range(0, self.width):
                    for row in range(0, self.height):
                        for voxel in range(0, self.width):
                            # get light value of last voxel, reduce it and add to lightarray
                            self.lightarray[layer,row,voxel]


                            # if visible[row,self.width-(layer+1)] == self.id_air:
                            #     visible[row,self.width-(layer+1)] = self.model[layer,row,voxel]

            if side == 'right':
                for layer in range(self.width-1,-1,-1):
                    for row in range(0, self.height):
                        for voxel in range(0, self.width):
                            # get light value of last voxel, reduce it and add to lightarray
                            self.lightarray[layer,row,voxel]

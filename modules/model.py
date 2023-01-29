import numpy as np
import anvil
from light import Light
from PIL import Image, ImageDraw

class Model:
    def __init__(self):
        self.light = Light('self.model.model')
        self.height = 0
        self.width = 0
        self.set_dimensions()
        self.model = np.zeros((self.width, self.height, self.width))

    # TODO: set dimension through config file
    def set_dimensions(self):
        'height and width must be in a 2:1 ratio'
        pass

    def save(self):
        """save model in file"""
        np.save('../saves/lightarr.npy', self.model)

    def load(self):
        """load lightarray from file"""
        self.model = np.load('../saves/lightarr.npy')

    def replace_with_air(self, material: str):
        if material not in self.config["materials"]:
            return
        for layer in range(0, self.width):
            for row in range(0, self.height):
                for voxel in range(0, self.width):
                    if self.model[layer][row][voxel] == self.config["materials"]["material"]:
                        self.model[layer][row][voxel] = self.config["materials"]["air"]

    def generate_images(self):
        sides = ['front', 'back', 'left', 'right']
        for side in sides:
            image = Image.new("RGB", (self.width, self.height), (0, 0, 0))
            d = ImageDraw.Draw(image)

            # array to save visible voxels
            visible = np.zeros((self.height, self.width))

            if side == 'front':
                # iterate through map and add visible voxels to array
                for layer in range(0, self.width):
                    for row in range(0, self.height):
                        for voxel in range(0, self.width):
                            # there is no voxel set, set new one 
                            if visible[row,voxel] == 0:
                                visible[row,voxel] = self.model[layer,row,voxel]
                
            if side == 'back':
                # iterate through map and add visible voxels to array
                for layer in range(self.width-1,-1,-1):
                    for row in range(0, self.height):
                        for voxel in range(0, self.width):
                            # there is no voxel set, set new one 
                            if visible[row,-voxel-1] == 0:
                                # 'mirror' voxel value, because of iteration from back
                                visible[row,-voxel-1] = self.model[layer,row,voxel]

            if side == 'left':
                for layer in range(0, self.width):
                    for row in range(0, self.height):
                        for voxel in range(0, self.width):
                            # if visible empty on this index, set to current voxel
                            if visible[row,self.width-(layer+1)] == 0:
                                visible[row,self.width-(layer+1)] = self.model[layer,row,voxel]

            if side == 'right':
                for layer in range(self.width-1,-1,-1):
                    for row in range(0, self.height):
                        for voxel in range(0, self.width):
                            # if visible empty on this index, set to current voxel
                            to_mirror = self.width-(layer+1)
                            if visible[row,-to_mirror-1] == 0:
                                visible[row,-to_mirror-1] = self.model[layer,row,voxel]

            # TODO: get material ids from config file
            # iterate through visible voxels and add them to image
            for row in range(0, self.height):
                for voxel in range(0, self.width):
                    if visible[row,voxel] == 1:
                        d.rectangle(((voxel, row), (voxel, row)), color_leaf)
                    elif visible[row,voxel] == 2:
                        d.rectangle(((voxel, row), (voxel, row)), color_wood)
            # reset visible
            visible = np.zeros((self.height, self.width))
            
            # save image to file
            image.save('images/'+side+'.png')

    # TODO: fix path, maybe add to config
    def model_minecraft(self, arr, path: str = "/Users/philippschuetz/Library/Application Support/minecraft/saves/Simulation/region/"):
        """
        load np array into a minecraft world

        height/width,depth ratio = 2/1
        """
        region = anvil.EmptyRegion(0, 0)

        AIR = anvil.Block('minecraft', 'air')
        WOOD = anvil.Block('minecraft', 'oak_wood')
        LEAF = anvil.Block('minecraft', 'oak_leaves', {"persistent": True})
        GREEN_CONCRETE = anvil.Block('minecraft', 'green_concrete')

        length = len(arr)*2

        # clear area
        for i in range(length):
            for j in range(length-1, -1, -1):
                for k in range(length):
                    region.set_block(AIR, k, (length-(j+1)), i)
        region.save(path + 'r.0.0.mca')

        # loop over 3d model and insert into region
        for i in range(int(length/2)):
            for j in range(length-1, -1, -1):
                for k in range(int(length/2)):
                    # leaf voxel
                    if arr[i, j, k] == 1:
                        region.set_block(LEAF, k, (length-(j+1)), i)
                    # wood voxel
                    elif arr[i, j, k] == 2:
                        region.set_block(WOOD, k, (length-(j+1)), i)
                    # light
                    elif arr[i, j, k] > 100:
                        region.set_block(WOOD, k, (length-(j+1)), i)

        region.save(path + 'r.0.0.mca')
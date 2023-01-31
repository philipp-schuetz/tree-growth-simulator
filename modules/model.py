import numpy as np
import anvil
import modules.config as config
import modules.light as light
from PIL import Image, ImageDraw
from pathlib import Path

class Model:
    def __init__(self):
        self.config = config.Config()
        self.light = light.Light()

        # create variable for model dimensions and set them with config
        self.width = 0
        self.height = 0
        self.set_dimensions()

        # get material ids from config
        ids = self.config.get_material_id()
        self.id_air = ids['air']
        self.id_leaf = ids['leaf']
        self.id_wood = ids['wood']
        self.id_wall = ids['wall']

        # create array for tree model
        self.model = np.zeros((self.width, self.height, self.width))

    def set_dimensions(self):
        'fetch and set model dimensions from config file'
        dimensions = self.config.get_model_dimensions()
        self.width = dimensions['width']
        self.height = dimensions['height']

    def save(self):
        """save model in file"""
        np.save('../saves/lightarr.npy', self.model)

    def load(self):
        """load lightarray from file"""
        self.model = np.load('../saves/lightarr.npy')

    def generate_images(self):
        # get colors from config
        colors = self.config.get_material_color()
        color_leaf = tuple(colors['leaf'])
        color_wood = tuple(colors['wood'])

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
                            if visible[row,voxel] == self.id_air:
                                visible[row,voxel] = self.model[layer,row,voxel]
                
            if side == 'back':
                # iterate through map and add visible voxels to array
                for layer in range(self.width-1,-1,-1):
                    for row in range(0, self.height):
                        for voxel in range(0, self.width):
                            # there is no voxel set, set new one 
                            if visible[row,-voxel-1] == self.id_air:
                                # 'mirror' voxel value, because of iteration from back
                                visible[row,-voxel-1] = self.model[layer,row,voxel]

            if side == 'left':
                for layer in range(0, self.width):
                    for row in range(0, self.height):
                        for voxel in range(0, self.width):
                            # if visible empty on this index, set to current voxel
                            if visible[row,self.width-(layer+1)] == self.id_air:
                                visible[row,self.width-(layer+1)] = self.model[layer,row,voxel]

            if side == 'right':
                for layer in range(self.width-1,-1,-1):
                    for row in range(0, self.height):
                        for voxel in range(0, self.width):
                            # if visible empty on this index, set to current voxel
                            to_mirror = self.width-(layer+1)
                            if visible[row,-to_mirror-1] == self.id_air:
                                visible[row,-to_mirror-1] = self.model[layer,row,voxel]

            # iterate through visible voxels and add them to image
            for row in range(0, self.height):
                for voxel in range(0, self.width):
                    if visible[row,voxel] == self.id_leaf:
                        d.rectangle(((voxel, row), (voxel, row)), color_leaf)
                    elif visible[row,voxel] == self.id_wood:
                        d.rectangle(((voxel, row), (voxel, row)), color_wood)
            # reset visible
            visible = np.zeros((self.height, self.width))
            
            
            # check if output path exists, otherwise create
            out_dir = Path('images')
            if not out_dir.is_dir():
                out_dir.mkdir(parents=True, exist_ok=True)

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
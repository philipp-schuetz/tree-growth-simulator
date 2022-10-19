import numpy as np
import mcmodel

def cprint(content):
    STARTC = '\033[94m'
    ENDC = '\033[0m'
    print(f"{STARTC}{content}{ENDC}")

class Tree:
    def __init__(self):
        # standart percent values
        self.water_provided = 100
        self.light_provided = 100

        self.paused = False

        # daily water needed before completion if first growth period (1 year) in litres (<200cm, 200-400cm, 400-600cm)
        # watering frequency depends on ground type and is only necessary for leaf/needle carrying trees
        # https://www.greenmax.eu/cms/news/525/173/Wie-viel-Wasser-braucht-ein-Baum/d,detail_2016/
        self.water_needed_p1 = ((3, 5), (5, 15), (10, 25))

    def pause(self):
        self.paused = not self.paused

    def get_touching_voxel_2d_material(self, arr, layer, row, voxel):
        voxel_next_to_2d_material = []
        try:
            voxel_next_to_2d_material.append(arr[layer, row, voxel-1])
        except IndexError:
            voxel_next_to_2d_material.append(0)
        try:
            voxel_next_to_2d_material.append(arr[layer, row, voxel+1])
        except IndexError:
            voxel_next_to_2d_material.append(0)
        try:
            voxel_next_to_2d_material.append(arr[layer, row-1, voxel])
        except IndexError:
            voxel_next_to_2d_material.append(0)
        try:
            voxel_next_to_2d_material.append(arr[layer, row-1, voxel])
        except IndexError:
            voxel_next_to_2d_material.append(0)
        return voxel_next_to_2d_material

    # sides: front, back, left, right, top, bottom
    def calc_lightlevel(self, light:tuple, map, materials:dict):
        if len(light) > 6:
            return
        layers = len(map)
        lightmap = np.zeros((layers, layers, layers, 6))

        # front
        for layer in range(layers):
            for row in range(layers):
                for voxel in range(layers):
                    # check if layer is outer layer
                    if layer != 0:
                        lightmap[layer, row, voxel, 0] = lightmap[layer-1, row, voxel, 1]
                    else:
                        lightmap[layer, row, voxel, 0] = light[0]
                    
                    # set back of voxel
                    light_new = (lightmap[layer, row, voxel, 0] * materials[map[layer, row, voxel]]) / 100
                    lightmap[layer, row, voxel, 1] = light_new

        # back
        for layer in range(layers-1, -1, -1):
            for row in range(layers):
                for voxel in range(layers):
                    # check if layer is outer layer
                    if layer != layers-1:
                        lightmap[layer, row, voxel, 1] = lightmap[layer+1, row, voxel, 1]
                    else:
                        lightmap[layer, row, voxel, 1] = light[1]
                    
                    # set front of voxel
                    light_new = (lightmap[layer, row, voxel, 1] * materials[map[layer, row, voxel]]) / 100
                    lightmap[layer, row, voxel, 0] = light_new

        # left
        for layer in range(layers-1, -1, -1):
            for row in range(layers):
                for voxel in range(layers):
                    # check if layer is outer layer
                    if layer != layers-1:
                        lightmap[layer, row, voxel, 1] = lightmap[layer+1, row, voxel, 1]
                    else:
                        lightmap[layer, row, voxel, 1] = light[1]
                    
                    # set front of voxel
                    light_new = (lightmap[layer, row, voxel, 1] * materials[map[layer, row, voxel]]) / 100
                    lightmap[layer, row, voxel, 0] = light_new
        
        return lightmap

tree = Tree()

np_map = np.zeros((4, 4, 4))
np_map[0][1][3] = 1
np_map[0][2][3] = 2
np_map[0][2][2] = 1
np_map[1][2][0] = 1
np_map[3][1][1] = 1

materials = {
    0: 100,
    1: 50,
    2: 0
}

lightinput = (100, 100, 100, 100, 100, 100)

print(tree.calc_lightlevel(lightinput, np_map, materials))
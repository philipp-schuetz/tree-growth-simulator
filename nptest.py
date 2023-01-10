import numpy as np
from modules import functions


def calc_lightlevel(light: int, map, translucence: dict):
    layers = len(map)
    lightmap = np.zeros_like(map)
    # front
    for layer in range(0, layers):
        # 100% light on outer layer
        if layer == 0:
            lightmap[layer] = light
        # every layer not on the outside
        else:
            for row in range(0, layers):
                for voxel in range(0, layers):
                    lightmap[layer][row][voxel] = lightmap[layer-1][row][voxel] * \
                        (translucence[map[layer-1][row][voxel]]/100)

    # back
    for layer in range(layers-1, -1, -1):
        # 100% light on outer layer
        if layer == layers-1:
            lightmap[layer] = light
        else:
            # every layer not on the outside
            for row in range(0, layers):
                for voxel in range(0, layers):
                    new_val = lightmap[layer+1][row][voxel] * \
                        (translucence[map[layer+1][row][voxel]]/100)
                    lightmap[layer][row][voxel] += new_val

    # left
    for layer in range(0, layers):
        for row in range(0, layers):
            for voxel in range(0, layers):
                # 100% light on outer layer
                if voxel == 0:
                    lightmap[layer][row][voxel] = light
                else:
                    new_val = lightmap[layer][row][voxel-1] * \
                        (translucence[map[layer][row][voxel-1]]/100)
                    lightmap[layer][row][voxel] += new_val

    # right
    for layer in range(0, layers):
        for row in range(0, layers):
            for voxel in range(layers-1, -1, -1):
                # 100% light on outer layer
                if voxel == 7:
                    lightmap[layer][row][voxel] = light
                else:
                    new_val = lightmap[layer][row][voxel+1] * \
                        (translucence[map[layer][row][voxel+1]]/100)
                    lightmap[layer][row][voxel] += new_val

    # # top
    # for layer in range(0, layers):
    return lightmap


# np_map = np.zeros((8, 8, 8))
np_map = np.zeros((25, 50, 25))

# material id, light modifier
# air, non-solid, solid
t_dict = {
    0: 100,
    1: 50,
    2: 0
}

lightarr = calc_lightlevel(100, np_map, t_dict)

# TODO: calc light from top


functions.model_minecraft(lightarr)

np.arange()

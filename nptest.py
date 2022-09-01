#!/usr/local/bin python3.9

import numpy as np

def calc_lightlevel(light:int, map, side:int, translucence:dict):
    layers = len(map)
    lightmap = np.zeros_like(map)
    # front
    if side == 0:
        for i in range(0, layers):
            # 100% light on outer layer
            if i == 0:
                lightmap[i] = light
            # every layer not on the outside
            else:
                for j in range(0, layers):
                    for k in range(0, layers):
                        if map[i-1][j][k] in translucence:
                            lightmap[i][j][k] = lightmap[i-1][j][k] * (translucence[map[i-1][j][k]]/100)
                        else:
                            return "E01"

    # back
    elif side == 1:
        for i in range(layers-1, -1, -1):
            # 100% light on outer layer
            if i == layers-1:
                lightmap[i] = light
            else:
                # every layer not on the outside
                for j in range(0, layers):
                    for k in range(0, layers):
                        if map[i+1][j][k] in translucence:
                            new_val = lightmap[i+1][j][k] * (translucence[map[i+1][j][k]]/100)
                            if new_val > lightmap[i][j][k]:
                                lightmap[i][j][k] = new_val
                        else:
                            return "E01"

    # left
    elif side == 2:
        for i in range(0, layers):
            for j in range(0, layers):
                for k in range(0, layers):
                    # 100% light on outer layer
                    if k == 0:
                        lightmap[i][j][k] = light
                    else:
                        if map[i][j][k-1] in translucence:
                            new_val = lightmap[i][j][k-1] * (translucence[map[i][j][k-1]]/100)
                            if new_val > lightmap[i][j][k]:
                                lightmap[i][j][k] = new_val
                        else:
                            return "E01"

    # right
    elif side == 3:
        for i in range(0, layers):
            for j in range(0, layers):
                for k in range(layers-1, -1, -1):
                    # 100% light on outer layer
                    if k == 7:
                        lightmap[i][j][k] = light
                    else:
                        if map[i][j][k+1] in translucence:
                            new_val = lightmap[i][j][k+1] * (translucence[map[i][j][k+1]]/100)
                            if new_val > lightmap[i][j][k]:
                                lightmap[i][j][k] = new_val
                        else:
                            return "E01"


    return lightmap

# air, not solid, solid
v_types = [[0,100],[1,50],[2,0]]


np_map = np.zeros((8, 8, 8))

np_map[0][1][7] = 1
np_map[0][2][7] = 1
np_map[0][4][6] = 1
np_map[1][2][5] = 1
np_map[3][1][7] = 1

t_dict = {
    0: 100,
    1: 50,
    2: 0
}

# print(np_map)
# input()
print(calc_lightlevel(100, np_map, 3, t_dict))

# Error:
# 0 = Error with light calc
#   1 = Material in given map doesn't exist

# TODO: calc light from top
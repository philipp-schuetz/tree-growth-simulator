import anvil
import numpy as np

region = anvil.EmptyRegion(0, 0)

WOOD = anvil.Block('minecraft', 'oak_wood')
LEAVES = anvil.Block('minecraft', 'oak_leaves', {"persistent": True})

np_map = np.zeros((8, 8, 8))

# 0,0,0
np_map[0][7][0] = 1
# 0,1,0
np_map[0][6][0] = 2

length = len(np_map)

for i in range(length):
    for j in range(length-1, -1, -1):
        for k in range(length):
            # non-solid
            if np_map[i, j, k] == 1:
                region.set_block(LEAVES, k, (length-(j+1)), i)
            # solid
            elif np_map[i, j, k] == 2:
                region.set_block(WOOD, k, (length-(j+1)), i)




path = "/Users/philippschuetz/Library/Application Support/minecraft/saves/Simulation/region/"
region.save(path + 'r.0.0.mca')

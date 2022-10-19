import anvil

def model(arr):
    region = anvil.EmptyRegion(0, 0)

    WOOD = anvil.Block('minecraft', 'oak_wood')
    LEAVES = anvil.Block('minecraft', 'oak_leaves', {"persistent": True})

    length = len(arr)

    for i in range(length):
        for j in range(length-1, -1, -1):
            for k in range(length):
                # non-solid
                if arr[i, j, k] == 1:
                    region.set_block(LEAVES, k, (length-(j+1)), i)
                # solid
                elif arr[i, j, k] == 2:
                    region.set_block(WOOD, k, (length-(j+1)), i)


    path = "/Users/philippschuetz/Library/Application Support/minecraft/saves/Simulation/region/"
    region.save(path + 'r.0.0.mca')

import anvil

def model_minecraft(arr, path: str = "/Users/philippschuetz/Library/Application Support/minecraft/saves/Simulation/region/"):
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
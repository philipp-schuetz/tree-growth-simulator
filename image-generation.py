from PIL import Image, ImageDraw, ImageFont
import numpy as np

sides = ['front', 'back', 'left', 'right']
width = 4
height = 8
array = np.zeros((width, height, width))
color_wood = (139,69,19)
color_leaf = (0,128,0)
leaf_id = 1
wood_id = 2


array[0][0][0] = 1
array[1][1][1] = 1
array[2][2][2] = 1
array[3][3][3] = 1


for side in sides:
    image = Image.new("RGB", (width, height), (0, 0, 0))
    d = ImageDraw.Draw(image)

    # array to save visible voxels
    visible = np.zeros((height, width))

    if side == 'front':
        # iterate through map and add visible voxels to array
        for layer in range(0, width):
            for row in range(0, height):
                for voxel in range(0, width):
                    # there is no voxel set, set new one 
                    if visible[row,voxel] == 0:
                        visible[row,voxel] = array[layer,row,voxel]
        
    if side == 'back':
        # iterate through map and add visible voxels to array
        for layer in range(width-1,-1,-1):
            for row in range(0, height):
                for voxel in range(0, width):
                    # there is no voxel set, set new one 
                    if visible[row,-voxel-1] == 0:
                        # 'mirror' voxel value, because of iteration from back
                        visible[row,-voxel-1] = array[layer,row,voxel]

    if side == 'left':
        for layer in range(0, width):
            for row in range(0, height):
                for voxel in range(0, width):
                    # if visible empty on this index, set to current voxel
                    if visible[row,width-(layer+1)] == 0:
                        visible[row,width-(layer+1)] = array[layer,row,voxel]

    if side == 'right':
        for layer in range(width-1,-1,-1):
            for row in range(0, height):
                for voxel in range(0, width):
                    # if visible empty on this index, set to current voxel
                    to_mirror = width-(layer+1)
                    if visible[row,-to_mirror-1] == 0:
                        visible[row,-to_mirror-1] = array[layer,row,voxel]

    # TODO: get material ids from config file
    # iterate through visible voxels and add them to image
    for row in range(0, height):
        for voxel in range(0, width):
            if visible[row,voxel] == 1:
                d.rectangle(((voxel, row), (voxel, row)), color_leaf)
            elif visible[row,voxel] == 2:
                d.rectangle(((voxel, row), (voxel, row)), color_wood)
    # reset visible
    visible = np.zeros((height, width))
    
    # save image to file
    image.save('images/'+side+'.png')

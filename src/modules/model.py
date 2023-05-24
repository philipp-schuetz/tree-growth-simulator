import numpy as np
from modules.config import config
import modules.light as light
from PIL import Image, ImageDraw
from pathlib import Path
import random
import matplotlib.pyplot as plt
# from mpl_toolkits.mplot3d import Axes3D

class Model:
    def __init__(self):
        # create variable for model dimensions and set them with config
        self.width = -1
        self.height = -1
        self.set_dimensions()

        # get material ids from config
        ids = config.get_material_id()
        self.id_air = ids['air']
        self.id_leaf = ids['leaf']
        self.id_wood = ids['wood']
        self.id_wall = ids['wall']

        # create array for tree model
        self.model = np.zeros((self.width, self.height, self.width))

        # modifiers
        self.water = -1
        self.temperature = -1
        self.nutrients = -1

        # base material and radius for tree generation
        self.material = self.id_wood
        self.radius = config.get_radius()

        # set first positions
        self.start_position = [int(self.width/2+0.5), self.height-1, int(self.width/2+0.5)]
        self.current_direction = 0
        self.position = self.start_position

        self.saved_position = []
        self.saved_direction = []
        self.saved_radius = []

        self.light = light.Light(self.model)

    def set_light_sides(self, sides: list[bool]):
        """format of sides: [front, back, left, right, top]"""
        self.light.activated_sides = ['front','back','left','right','top']
        to_remove = []
        for i in range(0, len(sides)):
            if not sides[i]:
                to_remove.append(self.light.activated_sides[i])
        for item in to_remove:
            self.light.activated_sides.remove(item)

    def set_dimensions(self):
        'fetch and set model dimensions from config file'
        dimensions = config.get_model_dimensions()
        self.width = dimensions['width']
        self.height = dimensions['height']
    
    def set_modifiers(self, light:int, water:int, temperature:int, nutrients:int):
        """set modifiers from ui"""
        self.water = water
        self.temperature = temperature
        self.nutrients = nutrients

        self.light.set_light(light)

    def save(self):
        """save model in file"""
        np.save('../saves/lightarr.npy', self.model)

    def load(self):
        """load lightarray from file"""
        self.model = np.load('../saves/lightarr.npy')


    # ---------------- l-system ----------------

    # cut the forward move length in half every time


    def place_voxel(self):
        """set current voxel(s) to specified material"""
        if self.radius > 0:
            # row stays the same, radius defines the with of the tree
            for layer in range(self.position[0]-self.radius, self.position[0]+self.radius):
                for voxel in range(self.position[2]-self.radius, self.position[2]+self.radius):
                    self.model[layer,self.position[1],voxel] = self.material
        elif self.radius == 0:
            self.model[self.position[0],self.position[1],self.position[2]] = self.material
        else:
            raise ValueError("radius for voxel placement can't be nagative")
        
    def is_next_to(self, coordinates:tuple[int,int,int], material_id:int) -> bool:
        """return True if voxel has given material next to it"""
        try:
            # back
            if self.model[coordinates[0]-1,coordinates[1],coordinates[2]] == material_id:
                return True
            # front
            elif self.model[coordinates[0]+1,coordinates[1],coordinates[2]] == material_id:
                return True
            # bottom
            elif self.model[coordinates[0],coordinates[1]-1,coordinates[2]] == material_id:
                return True
            # top
            elif self.model[coordinates[0],coordinates[1]+1,coordinates[2]] == material_id:
                return True
            # left
            elif self.model[coordinates[0],coordinates[1],coordinates[2]-1] == material_id:
                return True
            # right
            elif self.model[coordinates[0],coordinates[1],coordinates[2]+1] == material_id:
                return True
            else:
                return False
        except IndexError:
            return False
        
    def forward(self):
        """move one voxel in the current direction"""
        match self.current_direction:
            case 0:# positive layer
                self.position[0] = self.position[0]+1
            case 1: # negative voxel
                self.position[2] = self.position[2]-1
            case 2:# negative layer
                self.position[0] = self.position[0]-1
            case 3: # positive voxel
                self.position[2] = self.position[2]+1
    
    def right(self):
        """turn right 90°"""
        self.current_direction += 1
        if self.current_direction > 3:   
            self.current_direction = 0

    def left(self):
        """turn left 90°"""
        self.current_direction -= 1
        if self.current_direction  < 0:
            self.current_direction = 3

    def up(self):
        """move up one voxel"""
        self.position[1] += 1
    
    def down(self):
        """move down one voxel"""
        self.position[1] -= 1
    
    def set_radius(self, amount:int):
        """change radius size by the set amount"""
        radius = self.radius
        radius += amount
        if self.radius >= 0:
            self.radius = radius
        else:
            return
    
    def save_position(self):
        """save current position"""
        self.saved_position.append(self.position)

    def get_position(self):
        """get the position last saved"""
        if len(self.saved_position) > 0:
            self.position = self.saved_position.pop(-1)

    def save_direction(self):
        """save current direction"""
        self.saved_direction.append(self.current_direction)

    def get_direction(self):
        """get the direction last saved"""
        if len(self.saved_direction) > 0:
            self.current_direction = self.saved_direction.pop(-1)
    
    def save_radius(self):
        """save current radius"""
        self.saved_position.append(self.radius)

    def get_radius(self):
        """get the radius last saved"""
        if len(self.saved_radius) > 0:
            self.radius = self.saved_radius.pop(-1)


    def generate_model(self):
        # TODO check values of all modifiers before generating
        # all generator values must reach a specific minimum (or maximum) value to start growing
        # reaching a specific value could add specific rules for generation or modify the iterations variable

        # ---- generate structure ----

        # ---- part1 - trunk ----
        # get initial radius from config



        # ---- generate leafs ----
        for layer in range(0, self.width):
            for row in range(0, self.height):
                for voxel in range(0, self.width):
                    # check if voxel is next to wood and minimum lightlevel is reached
                    if self.is_next_to((layer,row,voxel),self.id_wood) and self.light.lightarray[layer,row,voxel] >= config.get_minimum_light_level():
                        # add leaf
                        self.model[layer,row,voxel] = self.id_leaf
                        # recalculate lightlevel
                        self.light.calculate()
        print('done')

    # ---------------- display model ----------------
    def mathplotlib_plot(self):
        # Plot the resulting tree model
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        # Get the coordinates of the wood voxels
        x, y, z = np.where(self.model == self.id_wood)
        x1, y1, z1 = np.where(self.model == self.id_leaf)

        # Plot the wood voxels
        ax.scatter(x, y, z, c='brown', marker='s')
        ax.scatter(x1, y1, z1, c='green', marker='s')

        # Set the limits for the axes
        ax.set_xlim(0, self.model.shape[0])
        ax.set_ylim(0, self.model.shape[1])
        ax.set_zlim(0, self.model.shape[2])

        # Set labels for the axes
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')

        # Show the plot
        plt.show()

    def generate_images(self):
        # get colors from config
        colors = config.get_material_color()
        color_leaf = tuple(colors['leaf'])
        color_wood = tuple(colors['wood'])

        # only influences image generation and not model
        add_leafs = config.get_add_leafs()

        sides = ['front', 'back', 'left', 'right']
        
        # -------- image generation with leafs --------
        if add_leafs == True:
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
                out_dir = Path('images-leafs')
                if not out_dir.is_dir():
                    out_dir.mkdir(parents=True, exist_ok=True)

                # save image to file
                image.save('images-leafs/'+side+'.png')


        # -------- image generation without leafs --------
        if add_leafs != True:
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
                                # if visible empty or leaf on this index, set to current voxel
                                if visible[row,voxel] == self.id_air or visible[row,voxel] == self.id_leaf:
                                    visible[row,voxel] = self.model[layer,row,voxel]
                    
                if side == 'back':
                    # iterate through map and add visible voxels to array
                    for layer in range(self.width-1,-1,-1):
                        for row in range(0, self.height):
                            for voxel in range(0, self.width):
                                # if visible empty or leaf on this index, set to current voxel
                                if visible[row,-voxel-1] == self.id_air or visible[row,-voxel-1] == self.id_leaf:
                                    # 'mirror' voxel value, because of iteration from back
                                    visible[row,-voxel-1] = self.model[layer,row,voxel]

                if side == 'left':
                    for layer in range(0, self.width):
                        for row in range(0, self.height):
                            for voxel in range(0, self.width):
                                # if visible empty or leaf on this index, set to current voxel
                                if visible[row,self.width-(layer+1)] == self.id_air or visible[row,self.width-(layer+1)] == self.id_leaf:
                                    visible[row,self.width-(layer+1)] = self.model[layer,row,voxel]

                if side == 'right':
                    for layer in range(self.width-1,-1,-1):
                        for row in range(0, self.height):
                            for voxel in range(0, self.width):
                                # if visible empty or leaf on this index, set to current voxel
                                to_mirror = self.width-(layer+1)
                                if visible[row,-to_mirror-1] == self.id_air or visible[row,-to_mirror-1] == self.id_leaf:
                                    visible[row,-to_mirror-1] = self.model[layer,row,voxel]

                # iterate through visible voxels and add them to image
                for row in range(0, self.height):
                    for voxel in range(0, self.width):
                        if visible[row,voxel] == self.id_wood:
                            d.rectangle(((voxel, row), (voxel, row)), color_wood)
                # reset visible
                visible = np.zeros((self.height, self.width))
                
                
                # check if output path exists, otherwise create
                out_dir = Path('images-no-leafs')
                if not out_dir.is_dir():
                    out_dir.mkdir(parents=True, exist_ok=True)

                # save image to file
                image.save('images-no-leafs/'+side+'.png')
        
        print('images generated')

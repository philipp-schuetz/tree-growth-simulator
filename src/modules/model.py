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
        self.light_mod = -1
        self.water = -1
        self.temperature = -1
        self.nutrients = -1

        # minimum values
        self.minimum_light = -1
        self.minimum_water = -1
        self.minimum_temperature = -1
        self.minimum_nutrients = -1
        self.set_minimum_values()

        # base material and radius for tree generation
        self.material = self.id_wood
        self.radius = 0

        # set first positions
        self.start_position = [int(self.width/2+0.5), self.height-1, int(self.width/2+0.5)]
        self.current_direction = 0
        self.position = self.start_position.copy()

        self.saved_position = []
        self.saved_direction = []
        self.saved_radius = []

        self.radius_mode = 'trunk'

        self.light = light.Light()

    def set_minimum_values(self):
        """set minimum values for modifiers"""
        minimum_values = config.get_minimum_values()

        self.minimum_light = minimum_values[0]
        self.minimum_water = minimum_values[1]
        self.minimum_temperature = minimum_values[2]
        self.minimum_nutrients = minimum_values[3]

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
        self.light_mod = light
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
        try:
            if self.radius > 1:
                for layer in range(self.width):
                    for voxel in range(self.width):
                        distance = np.sqrt((layer - self.position[0])**2 + (voxel - self.position[2])**2)
                        if distance <= self.radius:
                            self.model[layer,self.position[1],voxel] = self.material
            elif self.radius == 1:
                self.model[self.position[0],self.position[1],self.position[2]] = self.material
            else:
                raise ValueError("radius for voxel placement can't be negative")
        except IndexError as e:
            # print(e)
            pass
        
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
            case 0:# positive layer - forward
                self.position[0] = self.position[0]+1
            case 1: # negative voxel - right
                self.position[2] = self.position[2]-1
            case 2:# negative layer - back
                self.position[0] = self.position[0]-1
            case 3: # positive voxel - left
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
        self.position[1] -= 1
    
    def down(self):
        """move down one voxel"""
        self.position[1] += 1
    
    def set_radius(self, amount:int):
        """change radius size by the set amount"""
        radius = self.radius
        radius += amount
        if radius >= 1:
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
        self.saved_radius.append(self.radius)

    def get_radius(self):
        """get the radius last saved"""
        if len(self.saved_radius) > 0:
            self.radius = self.saved_radius.pop(-1)
    
    def save_positioning(self):
        """save current position, direction and radius"""
        self.save_position()
        self.save_direction()
        self.save_radius()

    def get_positioning(self):
        """get saved position, direction and radius"""
        self.get_position()
        self.get_direction()
        self.get_radius()

    def is_within_bounds(self):
        """Check if the current position is within the bounds of the model"""
        x, y, z = self.position
        return 0 <= x < self.width and 0 <= y < self.height and 0 <= z < self.width
    
    def light_minimum_reached(self) -> bool:
        directions = [(-1, 0, 0), (1, 0, 0), (0, 0, -1), (0, 0, 1), (0, -1, 0)]
        # front back left right top
        if 'front' not in self.light.activated_sides:
            directions[0] = 0
        if 'back' not in self.light.activated_sides:
            directions[1] = 0
        if 'left' not in self.light.activated_sides:
            directions[2] = 0
        if 'right' not in self.light.activated_sides:
            directions[3] = 0
        if 'top' not in self.light.activated_sides:
            directions[4] = 0

        
        total_light = 0

        for direction in directions:
            if direction == 0:
                continue
            object_count = 0
            for x in range(1, 250):
                dx, dy, dz = direction
                new_x, new_y, new_z = self.position[0] + dx*x, self.position[1] + dy*x, self.position[2] + dz*x

                try:
                    if self.model[new_x,new_y,new_z] != 0:
                        object_count += 1
                except IndexError as e:
                    # print(f'light calc: {e}')
                    pass

            if object_count == 0:
                total_light += self.light_mod
        
        if total_light/2 >= self.minimum_light:
            return True
        else:
            return False


    def generate_model(self):
        self.radius = 5 # start_radius
        branch_length = 20
        iterations = 6
        min_branching_height = 40 # height at which branches start appearing

        # ---- calculate and apply modifiers ----
        # abort when minimum values are not reached
        if self.water < self.minimum_water or self.temperature < self.minimum_temperature or self.nutrients < self.minimum_nutrients:
            return

        if self.temperature/100 > 1:
            self.water *= self.temperature/100

        if self.water/100 <= 1.5:
            branch_length *= self.water/100
            min_branching_height *= self.water/100
        elif self.water/100 > 1.5:
            branch_length *= 1-self.water/100
            min_branching_height *= 1-self.water/100

        if self.nutrients/100 <= 1.5:
            branch_length *= self.nutrients/100
            min_branching_height *= self.nutrients/100
        elif self.nutrients/100 > 1.5:
            branch_length *= 1-self.nutrients/100
            min_branching_height *= 1-self.water/100


        branching_position = []
        branching_radius = []
        branching_position_tmp = []
        branching_radius_tmp = []
        
        # generate main trunk
        for i in range(int(min_branching_height)):
            self.place_voxel()
            self.up()
            if i % 20 == 0:
                self.set_radius(-1)
        branching_position.append(self.position)
        branching_radius.append(self.radius)
        
        # print(f'branch radius: {self.radius}')
        for i in range(iterations):
            random.shuffle(branching_position)
            # remove random items from the list
            # for x in range(int(len(branching_position)/4)):
            #     if i == 0:
            #         continue
            #     branching_position.pop(random.randrange(len(branching_position)))
            
            for bp in range(len(branching_position)):
                start_pos = branching_position[bp]
                start_radius = branching_radius[bp]

                for d in range(4):
                    # chance to skip branch
                    if random.randrange(128) == 0 and iterations < 2:
                        continue
                    elif random.randrange(6) == 0 and iterations >= 2 and iterations < 4:
                        continue
                    elif random.randrange(2) == 0 and iterations >= 4:
                        continue
                    
                    self.position = start_pos.copy()
                    self.radius = start_radius
                    self.current_direction = d
                    # branch_length += random.randrange(-2,i)
                    for m in range(int(branch_length)):
                        self.forward()
                        if not self.light_minimum_reached():
                            break
                        self.place_voxel()
                        for du in range(random.randrange(8)):
                            self.up()
                        for dd in range(random.randrange(4)):
                            self.down()
                        self.set_radius(-1)
                    # save branch end
                    branching_position_tmp.append(self.position)
                    branching_radius_tmp.append(self.radius)

            branching_position = branching_position_tmp.copy()
            branching_position_tmp = []
            branching_radius = branching_radius_tmp.copy()
            branching_radius_tmp = []


        # ---- generate leafs ---- code partly deprecated
        # for layer in range(0, self.width):
        #     for row in range(0, self.height):
        #         for voxel in range(0, self.width):
        #             # check if voxel is next to wood and minimum lightlevel is reached
        #             if self.is_next_to((layer,row,voxel),self.id_wood) and self.light.lightarray[layer,row,voxel] >= self.minimum_light:
        #                 # add leaf
        #                 self.model[layer,row,voxel] = self.id_leaf
        #                 # recalculate lightlevel
        #                 self.light.calculate()
        # print('images')
        # self.generate_images()
        # print('done')

    # ---------------- display model ----------------
    def mathplotlib_plot(self):
        # Plot the resulting tree model
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        # Get the coordinates of the wood voxels
        x, y, z = np.where(self.model == self.id_wood)
        x1, y1, z1 = np.where(self.model == self.id_leaf)

        # plot voxels with correct orientation
        ax.scatter(x, z, -y, c='brown', marker='s')
        ax.scatter(x1, z1, -y1, c='green', marker='s')

        # Set the limits for the axes
        ax.set_xlim(0, self.model.shape[0])
        ax.set_ylim(0, self.model.shape[2])
        ax.set_zlim(-self.model.shape[1], 0)

        # Set labels for the axes
        ax.set_xlabel('X')
        ax.set_ylabel('Z')
        ax.set_zlabel('Y')

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
        add_leafs = False
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

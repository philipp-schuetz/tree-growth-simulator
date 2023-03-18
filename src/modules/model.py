import numpy as np
import anvil
from modules.config import config
import modules.light as light
from PIL import Image, ImageDraw
from pathlib import Path
import random

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
        self.radius = 0

        self.sentence = '' # l-system sentence
        self.iterations = 0
        self.rules = {}

        # set first positions
        self.start_position = [int(self.width/2+0.5), self.height-1, int(self.width/2+0.5)]
        self.position = self.start_position
        self.positions = []

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
    
    def set_iterations(self):
        self.iterations = config.get_iterations()

    def set_start(self):
        self.sentence = config.get_start_letter()

    def set_rules(self):
        rules = config.get_rules()
        for rule in rules:
            if rule['letter'] not in self.rules:
                self.rules['letter'] = []
            self.rules[rule['letter']].append(rule['new_letters'])

    def save(self):
        """save model in file"""
        np.save('../saves/lightarr.npy', self.model)

    def load(self):
        """load lightarray from file"""
        self.model = np.load('../saves/lightarr.npy')


    # ---------------- l-system ----------------

    # cut the forward move length in half every time

    def apply_rules(self):
        """apply a rule for each character in the sentence (random rule if multiple exist)"""
        new_sentence = ''
        for letter in self.sentence:
            if letter in self.rules:
                new_sentence += random.choice(self.rules[letter])
            else:
                new_sentence += letter
        self.sentence = new_sentence

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

    def generate_model(self):
        for iteration in range(0, self.iterations):
            self.apply_rules()
            for letter in self.sentence:
                match letter:
                    case 'P':
                        self.place_voxel()
                    case 'l': # toward negative layer index
                        self.position[0] = self.position[0]-1
                    case 'L': # toward positive layer index
                        self.position[0] = self.position[0]+1
                    case 'v': # toward negative voxel index
                        self.position[2] = self.position[2]-1
                    case 'V': # toward positive voxel index
                        self.position[2] = self.position[2]+1
                    case 'c': # center Downward
                        self.position[1] = self.position[1]+1
                    case 'C': # center Upward
                        self.position[1] = self.position[1]-1
                    case 'r': # radius smaller
                        if self.radius != 0:
                            self.radius -= 1
                    case 'R': # radius larger
                        self.radius += 1
                    case '[': # save position
                        self.positions.append(self.position)
                    case ']': # get saved position
                        self.position = self.positions.pop(-1)

    # ---------------- display model ----------------

    def generate_images(self): #TODO generate images with and without leafes (different folders)
        # get colors from config
        colors = config.get_material_color()
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
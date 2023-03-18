import numpy as np
import string

# cut the forward move length in half every time
# TODO: retrieve configs for this script from config file later
class Actions():
    def __init__(self, height:int, width:int):

        self.material = 2
        self.base_width = 1
        self.autoplace = True # execute place function after every move if set to true
        # base radius for placing
        self.radius = 0

        self.actions = ['u3','f','b2','f','l','r2','re'] # actions to execute on run
        self.position = [] # current position
        self.positions = [] # saved positions

        # set first positions
        self.start_pos = [int(width/2+0.5), height-1, int(width/2+0.5)]
        self.position = self.start_pos
        self.positions = [self.start_pos]

        self.model = np.zeros((width, height, width))


    def place(self):
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

    def execute(self):
        action_type = ''
        action_repeat = 0
        for action in self.actions:
            for char in action:
                # sort actions in commands and repeats
                if char in string.ascii_lowercase:
                    action_type += char
                elif char in string.digits:
                    action_repeat += int(char)

            i = 0
            while i < action_repeat:
                match action_type:
                    case 'p':
                        self.place()
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

                if self.autoplace and action != 'p':
                    self.place()
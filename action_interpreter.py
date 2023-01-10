import numpy as np
import mcmodel
import string

# cut the forward move length in half every time
# TODO: retrieve configs for this script from config file later
class Actions():
    def __init__(self, height:int, width:int):

        self.material = 2
        self.base_width = 1
        self.autoplace = True # execute place function after every move if set to true

        self.actions = ['u3','f','b2','f','l','r2','re'] # actions to execute on run
        self.position = [] # current position
        self.positions = [] # saved positions

        # set first positions
        self.start_pos = [int(width/2), height-1, int(width/2)]
        self.position = self.start_pos
        self.positions = [self.start_pos]

        self.model = np.zeros((width, height, width))


    def place(self):
        'set current voxel to specified material'
        # TODO: place multiple voxels with one place method iteration
        for i in range(0, self.base_width*self.base_width):
            self.model[self.position[0],self.position[1],self.position[2]] = self.material
    def forward(self):
        'move forward one voxel'
        self.position[0] = self.position[0]+1
    def backward(self):
        'move backward one voxel'
        self.position[0] = self.position[0]-1
    def left(self):
        'move left one voxel'
        self.position[2] = self.position[2]-1  
    def right(self):
        'move right one voxel'
        self.position[2] = self.position[2]+1
    def up(self):
        'move up one voxel'
        self.position[1] = self.position[1]-1
    def down(self):
        self.position[1] = self.position[1]+1
    def save(self):
        'save current position'
        self.positions.append(self.position)
    def set(self):
        'set position to last saved position'
        self.position = self.positions[-1]
    def reset(self):
        'set position to start position'
        self.position = self.start_pos

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
                    case 'f':
                        self.forward()
                    case 'b':
                        self.backward()
                    case 'l':
                        self.left()
                    case 'r':
                        self.right()
                    case 'u':
                        self.up()
                    case 'd':
                        self.down()
                    case 'sa':
                        self.save()
                    case 'se':
                        self.set()
                    case 're':
                        self.reset()
                
                if self.autoplace and action != 'p':
                    self.place()
                i += 1

    def run(self):
        self.execute()
        mcmodel.model_minecraft(self.model)

actions = Actions(8, 4)

actions.run()
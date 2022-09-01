from ui import Ui
from tree import Tree

class App():
    def __init__(self):
        self.ui = Ui()
        self.tree = Tree()
    
    def __del__(self):
        del self.ui
        del self.tree

    def handle_input(self, key):
        if key == "q":
            return 0
        elif key == "p":
            self.tree.pause()
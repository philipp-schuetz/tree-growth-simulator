import numpy as np
from .ui import Ui
from .model import Model
from .light import Light
from .config import Config

# TODO: move light object to model, calculate after every set voxel

class App:
    def __init__(self):
        self.ui = Ui()
        self.model = Model('self.config')
        self.model.set_dimensions(500, 250)
        self.light = Light('self.model.model')

    def run(self):
        """run main event loop"""
        while self.ui.window_status == 1:
            self.ui.handle_window()

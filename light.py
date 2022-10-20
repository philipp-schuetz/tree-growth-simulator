import numpy as np
from typing import Union


class Light:
    def __init__(self, modelarray=None):
        """if modelarray isn't provided last save is pulled from a file"""
        self.translucence = {
            0: 100,
            1: 50,
            2: 0
        }
        if modelarray == None:
            self.lightarray = load_arr()
            self.layers = len(self.lightarray)
        else:
            self.lightarray = np.zeros_like(modelarray)
            self.layers = len(modelarray)


def calculate(self, baselight: Union[int, tuple[int, int, int, int, int]]):
    """calculates the lightvalue for each voxel"""
    return


def save_arr(self):
    """save lightarray in file"""
    np.save('./saves/lightarr.npy', self.lightarray)


def load_arr():
    """load lightarray from file"""
    return np.load('./saves/lightarr.npy')

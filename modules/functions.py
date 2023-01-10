import anvil
import numpy as np


def getindex(coords: tuple[int, int, int], array) -> tuple[int, int, int]:
    """conversion from x(plain),y(height),z(room) coordinates starting, at 0,0,0, to array indexes of 3d array"""
    for i in coords:
        if i >= len(array):
            raise IndexError('coordinates out of bounds')
    return (coords[2], len(array)-(coords[1]+1), coords[0])


def cprint(content):
    STARTC = '\033[94m'
    ENDC = '\033[0m'
    print(f"{STARTC}{content}{ENDC}")

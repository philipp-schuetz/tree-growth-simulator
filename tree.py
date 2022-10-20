import numpy as np
import mcmodel


class Tree:
    def __init__(self):
        # standart percent values
        self.water_provided = 100
        self.light_provided = 100

        self.paused = False

        # daily water needed before completion if first growth period (1 year) in litres (<200cm, 200-400cm, 400-600cm)
        # watering frequency depends on ground type and is only necessary for leaf/needle carrying trees
        # https://www.greenmax.eu/cms/news/525/173/Wie-viel-Wasser-braucht-ein-Baum/d,detail_2016/

    def pause(self):
        self.paused = not self.paused

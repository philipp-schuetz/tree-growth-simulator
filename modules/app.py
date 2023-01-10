import numpy as np
import json
import modules


class App:
    def __init__(self):
        self.config = self.load_config()
        self.model = modules.Model(self.config)
        self.model.set_dimensions(500, 250)
        light = modules.Light(self.model.model)
        ui = modules.Ui()
        ui.root.mainloop()

        # standart percent values
        self.water_provided = 
        self.light_provided = 100

        self.paused = False
        # daily water needed before completion if first growth period (1 year) in litres (<200cm, 200-400cm, 400-600cm)
        # watering frequency depends on ground type and is only necessary for leaf/needle carrying trees
        # https://www.greenmax.eu/cms/news/525/173/Wie-viel-Wasser-braucht-ein-Baum/d,detail_2016/

    def pause(self):
        self.paused = not self.paused

    def load_config(self):
        with open("../appdata/config.json", "r") as f:
            self.config = json.load(f)

    def run(self):
        while True:
            pass

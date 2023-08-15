"""Module contains the App class."""
from modules import ui
from modules import model
import logging

class App:
    """App contains ui, model and light objects and the mainloop of this application"""
    def __init__(self):
        logging.basicConfig(filename='logfile.log', level=logging.INFO, encoding='utf-8')
        self.ui = ui.Ui()
        self.model = model.Model()

    def run(self):
        """run main event loop"""
        while self.ui.window_status == 1:
            match self.ui.handle_window():
                case 'start':
                    self.model.set_modifiers(
                        self.ui.get_light(),
                        self.ui.get_water(),
                        self.ui.get_temperature(),
                        self.ui.get_nutrients()
                    )
                    self.model.set_light_sides(self.ui.get_light_sides())
                    self.model.set_leaf_generation(self.ui.get_leaf_generation())
                    self.model.set_save_to_image(self.ui.get_save_to_image())
                    self.model.generate_model()
                case 'show':
                    self.model.mathplotlib_plot()

    def api_run(self, request_id:str, light:int, water:int, temperature:int, nutrients:int, leafes:bool, light_sides:list[bool]):
        """run main event loop for execution through api"""
        self.model.set_modifiers(light, water, temperature, nutrients)
        self.model.set_api_id(id)
        self.model.set_light_sides(light_sides)
        self.model.set_leaf_generation(leafes)
        self.model.generate_model()
        self.model.mathplotlib_plot(True, request_id, True)

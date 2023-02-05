"""Module contains the App class."""
import modules.ui as ui
import modules.model as model

class App:
    """App contains ui, model and light objects and the mainloop of this application"""
    def __init__(self):
        self.ui = ui.Ui()
        self.model = model.Model()
        # self.model.set_dimensions(500, 250)

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
                case 'export':
                    self.model.generate_images()

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
                    pass
                case 'export':
                    self.model.generate_images()

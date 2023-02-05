import PySimpleGUI as sg
class Ui:
    """Ui class holds all ui elements"""
    def __init__(self) -> None:
        # 0 -> window closed, 1 -> window open
        self.window_status = 0

        # values of sliders: -1 -> unset
        self.value_light = -1
        self.value_water = -1
        self.value_temperature = -1
        self.value_nutrients = -1

        self.values_light_sides = [False, False, False, False, False]

        # set ui theme
        sg.theme('DarkBlue')

        # define ui layout
        self.layout = [
            [sg.Frame(title='Modifiers', layout=[
                [
                    sg.Text('Light in %'),
                    sg.Slider(range=(0,200), default_value=100, key='light', orientation='horizontal')
                ],
                [
                    sg.Checkbox('front', default=True, key='front'),
                    sg.Checkbox('back', default=True, key='back'),
                    sg.Checkbox('left', default=True, key='left'),
                    sg.Checkbox('right', default=True, key='right'),
                    sg.Checkbox('top', default=True, key='top')
                ],
                [
                    sg.Text('Water in %'),
                    sg.Slider(range=(0,200), default_value=100, key='water', orientation='horizontal')
                ],
                [
                    sg.Text('Temperature in %'),
                    sg.Slider(range=(0,200), default_value=100, key='temperature', orientation='horizontal')
                ],
                [
                    sg.Text('Nutrients in %'),
                    sg.Slider(range=(0,200), default_value=100, key='nutrients', orientation='horizontal')
                ]
            ]), sg.Frame(title='Buttons', layout=[
                [sg.Button('Start')],
                [sg.Button('Export to PNGs')]
            ])]
        ]

        # create window
        self.window = sg.Window('tree-growth-simulator', self.layout)
        self.window_status = 1

    def handle_window(self):
        """handle window events and values in the mainloop"""
        event, values = self.window.read()  # type: ignore

        # check for events
        match event:
            case 'Start':
                # save values
                self.value_light = values['light']
                self.value_water = values['water']
                self.value_temperature = values['temperature']
                self.value_nutrients = values['nutrients']

                self.values_light_sides = [
                    values['front'],
                    values['back'],
                    values['left'],
                    values['right'],
                    values['top']
                ]
                return 'start'
            case 'Export to PNGs':
                sg.popup('Please be patient while the images are being generated.', title='Export to PNGs')
                return 'export'
            case sg.WIN_CLOSED:
                self.close_window()

    def close_window(self) -> None:
        """close the currently active window"""
        self.window.close()
        self.window_status = 0

    def get_light(self) -> int:
        """get the light value"""
        return self.value_light

    def get_light_sides(self) -> list[bool]:
        """get the sides for which light calculation is activated"""
        return self.values_light_sides

    def get_water(self) -> int:
        """get the water value"""
        return self.value_water

    def get_temperature(self) -> int:
        """get the temperature value"""
        return self.value_temperature

    def get_nutrients(self) -> int:
        """get the nutrients value"""
        return self.value_nutrients

from tkinter import Tk, ttk, Scale, IntVar, Pack, HORIZONTAL


class Ui:
    def __init__(self) -> None:
        self.root = Tk()
        self.root.title("Tree Simulator")

        frame = ttk.Frame(self.root, padding="10")
        frame.grid(column=0, row=0)

        # add light slider
        self.val_light = IntVar()
        self.s1 = Scale(frame, from_=0, to=400, orient=HORIZONTAL,
                        digits=0, label="Water in %", variable=self.val_light).grid(column=0, row=1)
        # set to standard value
        self.val_light.set(100)

        # add water slider
        self.val_water = IntVar()
        self.s2 = Scale(frame, from_=0, to=400, orient=HORIZONTAL,
                        digits=0, label="Water in %", variable=self.val_water).grid(column=0, row=1)
        # set to standard value
        self.val_water.set(100)

        # add temperature slider
        self.val_temp = IntVar()
        self.s3 = Scale(frame, from_=0, to=400, orient=HORIZONTAL,
                        digits=0, label="Water in %", variable=self.val_temp).grid(column=0, row=1)
        # set to standard value
        self.val_temp.set(100)
        
        # add nutrients slider
        self.val_nutrients = IntVar()
        self.s4 = Scale(frame, from_=0, to=400, orient=HORIZONTAL,
                        digits=0, label="Water in %", variable=self.val_nutrients).grid(column=0, row=1)
        # set to standard value
        self.val_nutrients.set(100)


    def get_light(self):
        return self.val_light.get()

    def get_water(self):
        return self.val_water.get()

    def get_temperature(self):
        return self.val_temp.get()

    def get_nutrients(self):
        return self.val_nutrients.get()
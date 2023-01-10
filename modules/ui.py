from tkinter import Tk, ttk, Scale, IntVar, Pack, HORIZONTAL


class Ui:
    def __init__(self) -> None:
        self.root = Tk()
        self.root.title("Tree Simulator")

        frame = ttk.Frame(self.root, padding="10")
        frame.grid(column=0, row=0)

        self.val_water = IntVar()
        self.s1 = Scale(frame, from_=0, to=400, orient=HORIZONTAL,
                        digits=0, label="Water in %", variable=self.val_water).grid(column=0, row=1)

        self.val_water.set(100)

        self.val_water.get()
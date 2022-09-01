import curses

class Ui():
    def __init__(self):
        self.start()

        self.selection = [curses.A_UNDERLINE, curses.A_NORMAL]
        self.sel_menu_item = 0

        self.print_menu()

    def __del__(self):
        self.stop()

    def start(self):
        self.stdscr = curses.initscr()
        curses.noecho()
        curses.cbreak()
        curses.curs_set(False)
        self.stdscr.keypad(True)

    def stop(self):
        curses.nocbreak()
        self.stdscr.keypad(False)
        curses.curs_set(True)
        curses.echo()
        curses.endwin()
    
    def print_menu(self):
        self.stdscr.clear()
        self.stdscr.addstr(0, 0, f"Simulation Settings (% of optimum)", curses.A_BOLD)
        self.stdscr.addstr(2, 0, f"Water", selection[0])
        self.stdscr.addstr(3, 0, f"{tree.water_provided}%")
        self.stdscr.addstr(2, 8, f"Sunlight", selection[1])
        self.stdscr.addstr(3, 8, f"{tree.light_provided}%")
        self.stdscr.refresh()

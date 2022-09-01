import time
import curses
from app import App

app = App()

run = True
while run:
    key = app.ui.stdscr.getkey()
    handle_input = app.handle_input(key)

    if handle_input == 0:
        run = False

    elif key == 'KEY_LEFT':
        if selection[0] == curses.A_NORMAL:
            for i in range(len(selection)):
                if selection[i] == curses.A_UNDERLINE:
                    selection[i-1] = curses.A_UNDERLINE
                    selection[i] = curses.A_NORMAL
                    sel_menu_item = i-1
                    break
    elif key == 'KEY_RIGHT':
        if selection[len(selection)-1] == curses.A_NORMAL:
            for i in range(len(selection)):
                if selection[i] == curses.A_UNDERLINE:
                    selection[i+1] = curses.A_UNDERLINE
                    selection[i] = curses.A_NORMAL
                    sel_menu_item = i+1
                    break
    elif key == 'KEY_UP':
        if sel_menu_item == 0 and tree_obj.water_provided < 200:
            tree_obj.water_provided += 10
        if sel_menu_item == 1 and tree_obj.light_provided < 200:
            tree_obj.light_provided += 10
    elif key == 'KEY_DOWN':
        if sel_menu_item == 0 and tree_obj.water_provided > 0:
            tree_obj.water_provided -= 10
        if sel_menu_item == 1 and tree_obj.light_provided > 0:
            tree_obj.light_provided -= 10

del app
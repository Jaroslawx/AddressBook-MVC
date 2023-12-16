from utils.Log import logger
from Controllers.Controller import Controller
from Views.Textual.CLI import CLI
from Views.Graphical.GUI import GUI

import curses


def start_cli(stdscr):
    logger.log_info("Application started.")

    textual_view = CLI(stdscr)
    textual_view.display_start()


def start_gui():
    logger.log_info("Application started.")

    graphical_view = GUI()
    graphical_view.start_gui()


if __name__ == '__main__':
    choice = Controller.choose_interface_mode()
    if choice == "textual":
        curses.wrapper(start_cli)
    elif choice == "graphic":
        start_gui()
    elif choice == "exit":
        exit()
    else:
        choice = Controller.choose_interface_mode()

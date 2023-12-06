from utils.Log import logger
from Controllers.Controller import Controller
from Views.Textual.CLI import CLI
from Views.Graphical.GUI import graphical_view

import curses


# def main(stdscr):
#     logger.log_info("Application started.")
#
#     textual_view = CLI(stdscr)
#     textual_view.display_start()
#
#
# curses.wrapper(main)
#
# if __name__ == '__main__':
#     main(stdscr=curses.initscr())

def main():
    logger.log_info("Application started.")

    graphical_view.start_gui()


if __name__ == '__main__':
    main()

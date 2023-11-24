from utils.Log import logger
from Views.Textual.Interface import textual_view

import curses


def main(stdscr):
    logger.log_info("Application started.")

    if textual_view.display_start(stdscr) == 1:
        while True:
            textual_view.display_menu(stdscr)


curses.wrapper(main)

if __name__ == '__main__':
    main(stdscr=curses.initscr())



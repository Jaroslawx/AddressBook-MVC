from utils.Log import logger
import curses


class Functions:
    @staticmethod
    def display_options(stdscr, options, y, x, selected_option):
        # Print options
        for i, option in enumerate(options):
            if i == selected_option:
                stdscr.addstr(y + i, x, f"> {option}", curses.A_BOLD)
            else:
                stdscr.addstr(y + i, x, f"> {option}")

    @staticmethod
    def display_info(message):
        # Create a new window for the info message
        info_window = curses.newwin(5, 35, curses.LINES // 2 - 2, curses.COLS // 2 - 20)
        info_window.border(0)
        info_window.addstr(2, 1, message, curses.A_BOLD)
        logger.log_info(message)
        info_window.refresh()
        info_window.getch()
        info_window.clear()

    @staticmethod
    def input_text(stdscr, message, old=''):
        stdscr.clear()
        stdscr.refresh()
        curses.echo()
        curses.curs_set(1)

        input_window = curses.newwin(0, 0, curses.LINES // 2 - 5, 0)
        input_window.border(0)
        input_window.addstr(2, 2, f"Previous: {old}", curses.A_REVERSE)
        input_window.addstr(4, 2, message)
        input_window.refresh()

        text = input_window.getstr(4, len(message) + 3).decode('utf-8')

        curses.noecho()
        curses.curs_set(0)

        return text

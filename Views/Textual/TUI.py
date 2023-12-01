from utils.Log import logger
from Controllers.FileController import FileController
from Models.Trivia import trivia
from Views.Textual.Functions import Functions

import curses
import threading
import time
import datetime


class TUI:
    def __init__(self):
        self.stop_flag = threading.Event()

    @staticmethod
    def choose_interface_mode(stdscr):
        logger.log_info("Choose interface mode loaded.")

        # Setting the text cursor mode and waiting for input mode
        curses.curs_set(0)
        curses.noecho()
        stdscr.nodelay(0)

        # Set color
        curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.color_pair(1)

        # Console sizes download
        height, width = stdscr.getmaxyx()

        # Welcome communicate
        welcome_message = "Welcome to Address Book"
        # Position calculating
        x = (width - len(welcome_message)) // 2
        y = height // 3

        # Print welcome message
        stdscr.addstr(y, x, welcome_message, curses.color_pair(1) | curses.A_BOLD)
        stdscr.refresh()

        # Menu options
        start_options = ["Textual", "Graphical"]
        selected_option = 0

        # Welcome communicate
        input_message = "Choose view mode..."
        # Position calculating
        x = (width - len(input_message)) // 2 - 1
        y = height // 2

        stdscr.addstr(y + 2, x, input_message, curses.A_BLINK)
        stdscr.refresh()

        x = (width - len(welcome_message)) // 2
        y = (height // 3) + 3

        # Waiting for Enter
        while True:
            # Print start menu options
            Functions.display_options(stdscr, start_options, y, x, selected_option)

            stdscr.refresh()
            key = stdscr.getch()

            if key == curses.KEY_DOWN:
                selected_option = (selected_option + 1) % len(start_options)
            elif key == curses.KEY_UP:
                selected_option = (selected_option - 1) % len(start_options)
            elif key == 10:  # Enter
                if selected_option == 0:
                    # textual
                    return "textual"
                if selected_option == 1:
                    # graphical
                    return "graphical"

    @staticmethod
    def display_start(stdscr):
        logger.log_info("Entry screen loaded.")

        stdscr.clear()
        stdscr.refresh()

        # Set color
        curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.color_pair(1)

        # Console sizes download
        height, width = stdscr.getmaxyx()

        # Welcome communicate
        welcome_message = "Address Book"
        # Position calculating
        x = (width - len(welcome_message)) // 2
        y = height // 3

        # Print welcome message
        stdscr.addstr(y, x, welcome_message, curses.color_pair(1) | curses.A_BOLD)
        stdscr.refresh()

        # Menu options
        start_options = ["Start", "Load contacts"]
        selected_option = 0

        # Welcome communicate
        input_message = "Choose option..."
        # Position calculating
        x = (width - len(input_message)) // 2
        y = height // 2

        stdscr.addstr(y + 2, x, input_message, curses.A_BLINK)
        stdscr.refresh()

        x = (width - len(welcome_message)) // 2
        y = (height // 3) + 3

        # Waiting for Enter
        while True:
            # Print start menu options
            Functions.display_options(stdscr, start_options, y, x, selected_option)

            stdscr.refresh()
            key = stdscr.getch()

            if key == curses.KEY_DOWN:
                selected_option = (selected_option + 1) % len(start_options)
            elif key == curses.KEY_UP:
                selected_option = (selected_option - 1) % len(start_options)
            elif key == 10:  # Enter
                if selected_option == 0:
                    # Start
                    return 1
                if selected_option == 1:
                    # Load contacts and start
                    FileController.load_contacts_and_add()
                    return 1

    def display_date(self, date_window, fun_fact):
        while not self.stop_flag.is_set():
            date_window.clear()
            date_window.border(0)
            date_window.addstr(1, 1, "Date: " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            date_window.addstr(3, 1, fun_fact, curses.A_BOLD)
            # TODO: Trivia goes on frame, have to fix.
            date_window.refresh()
            time.sleep(1)

    def display_menu(self, stdscr):
        logger.log_info("Menu loaded.")
        stdscr.clear()
        stdscr.refresh()

        # Create windows for menu and date
        date_window = curses.newwin(7, curses.COLS, 0, 0)
        menu_window = stdscr.subwin(13, 30, 8, 0)

        # Menu options
        menu_options = ["1. Add contact", "2. Remove contact", "3. Display contacts", "4. Sort contacts",
                        "5. Edit contact", "6. Clear contacts", "7. Recycle bin", "X. Exit"]
        selected_option = 0

        fun_fact = trivia.get_random_trivia()

        while True:
            stdscr.clear()
            stdscr.refresh()

            # Start a thread to continuously refresh the date
            self.stop_flag.clear()
            date_thread = threading.Thread(target=self.display_date, args=(date_window, fun_fact))
            date_thread.start()

            # Menu communicate:
            message = "Menu:"
            menu_window.addstr(1, 1, message, curses.A_BOLD)
            menu_window.border(0)

            # Print menu options
            Functions.display_options(menu_window, menu_options, 3, 2, selected_option)

            key = menu_window.getch()
            menu_window.border(0)
            menu_window.refresh()

            if key == curses.KEY_DOWN:
                selected_option = (selected_option + 1) % len(menu_options)
            elif key == curses.KEY_UP:
                selected_option = (selected_option - 1) % len(menu_options)
            elif key == 10:  #
                self.stop_flag.set()
                date_thread.join()

                if selected_option == 0:
                    # Handle the selected "Add contact" option
                    Functions.display_add_contact(stdscr)

                elif selected_option == 1:
                    # Handle the selected "Remove contact" option
                    Functions.display_remove_contact(stdscr)
                    pass
                elif selected_option == 2:
                    # Handle the selected "Display contacts" option
                    Functions.display_contacts(stdscr)

                elif selected_option == 3:
                    # Handle the selected "Sort contacts" option
                    Functions.display_sort_contacts(stdscr)

                elif selected_option == 4:
                    # Handle the selected "Edit contact" option
                    Functions.display_edit_contact(stdscr)

                elif selected_option == 5:
                    # Handle the selected "Clear contacts" option
                    Functions.clear_contacts_list()

                elif selected_option == 6:
                    # Handle the selected "Recycle bin" option
                    Functions.display_recycle_bin(stdscr)

                elif selected_option == 7:
                    # Handle the selected "Exit" option
                    Functions.display_exit(stdscr)


textual_view = TUI()

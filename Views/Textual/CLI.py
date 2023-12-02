from utils.Log import logger
from Controllers.FileController import FileController
from Models.Trivia import trivia
from Views.Textual.Functions import Functions

import curses
import threading
import time
import datetime


class CLI:
    def __init__(self, stdscr):
        self.stop_flag = threading.Event()
        self.stdscr = stdscr

    def display_start(self):
        logger.log_info("Entry screen loaded.")

        self.stdscr.clear()
        self.stdscr.refresh()

        # Set color
        curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.color_pair(1)

        # Console sizes download
        height, width = self.stdscr.getmaxyx()

        # Welcome communicate
        welcome_message = "Address Book"
        # Position calculating
        x = (width - len(welcome_message)) // 2
        y = height // 3

        # Print welcome message
        self.stdscr.addstr(y, x, welcome_message, curses.color_pair(1) | curses.A_BOLD)
        self.stdscr.refresh()

        # Menu options
        start_options = ["Start", "Load contacts"]
        selected_option = 0

        # Welcome communicate
        input_message = "Choose option..."
        # Position calculating
        x = (width - len(input_message)) // 2
        y = height // 2

        self.stdscr.addstr(y + 2, x, input_message, curses.A_BLINK)
        self.stdscr.refresh()

        x = (width - len(welcome_message)) // 2
        y = (height // 3) + 3

        # Waiting for Enter
        while True:
            # Print start menu options
            Functions.display_options(self.stdscr, start_options, y, x, selected_option)

            self.stdscr.refresh()
            key = self.stdscr.getch()

            if key == curses.KEY_DOWN:
                selected_option = (selected_option + 1) % len(start_options)
            elif key == curses.KEY_UP:
                selected_option = (selected_option - 1) % len(start_options)
            elif key == 10:  # Enter
                if selected_option == 0:
                    # Start
                    CLI.display_menu(self)
                if selected_option == 1:
                    # Load contacts and start
                    FileController.load_contacts_and_add()
                    CLI.display_menu(self)

    def display_date(self, date_window, fun_fact):
        while not self.stop_flag.is_set():
            date_window.clear()
            date_window.border(0)
            date_window.addstr(1, 1, "Date: " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            date_window.addstr(3, 1, fun_fact, curses.A_BOLD)
            # TODO: Trivia goes on frame, have to fix.
            date_window.refresh()
            time.sleep(1)

    def display_menu(self):
        logger.log_info("Menu loaded.")
        self.stdscr.clear()
        self.stdscr.refresh()

        # Create windows for menu and date
        date_window = curses.newwin(7, curses.COLS, 0, 0)
        menu_window = self.stdscr.subwin(13, 30, 8, 0)

        # Menu options
        menu_options = ["1. Add contact", "2. Remove contact", "3. Display contacts", "4. Sort contacts",
                        "5. Edit contact", "6. Clear contacts", "7. Recycle bin", "X. Exit"]
        selected_option = 0

        fun_fact = trivia.get_random_trivia()

        while True:
            self.stdscr.clear()
            self.stdscr.refresh()

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
                    Functions.display_add_contact(self.stdscr)

                elif selected_option == 1:
                    # Handle the selected "Remove contact" option
                    Functions.display_remove_contact(self.stdscr)
                    pass
                elif selected_option == 2:
                    # Handle the selected "Display contacts" option
                    Functions.display_contacts(self.stdscr)

                elif selected_option == 3:
                    # Handle the selected "Sort contacts" option
                    Functions.display_sort_contacts(self.stdscr)

                elif selected_option == 4:
                    # Handle the selected "Edit contact" option
                    Functions.display_edit_contact(self.stdscr)

                elif selected_option == 5:
                    # Handle the selected "Clear contacts" option
                    Functions.clear_contacts_list()

                elif selected_option == 6:
                    # Handle the selected "Recycle bin" option
                    Functions.display_recycle_bin(self.stdscr)

                elif selected_option == 7:
                    # Handle the selected "Exit" option
                    Functions.display_exit(self.stdscr)

    def start_tui(self):
        logger.log_info("Application started in textual mode")

        CLI.display_start(self)

from utils.Log import logger
from Models.AddressBook import address_book
from Controllers.ContactController import ContactController
from Controllers.FileController import FileController
from prettytable import PrettyTable

import curses
import sys


class CLIFunctions:
    @staticmethod
    def display_options(window, options, y, x, selected_option):
        # Print options
        for i, option in enumerate(options):
            if i == selected_option:
                window.addstr(y + i, x, f"> {option}", curses.A_BOLD)
            else:
                window.addstr(y + i, x, f"> {option}")

    @staticmethod
    def display_info(message):
        # Create a new window for the info message
        info_window = curses.newwin(5, 35, curses.LINES // 2 - 2, curses.COLS // 2 - 20)
        info_window.border(0)
        info_window.addstr(2, 1, message, curses.A_BOLD)
        info_window.getch()
        info_window.clear()
        info_window.refresh()

    @staticmethod
    def display_list(window, contacts, start, rows, index, type_message, info_message):
        window.clear()
        window.refresh()

        window.border(0)

        window.addstr(1, 1, type_message, curses.A_BOLD)
        window.addstr(2, 2, info_message, curses.A_REVERSE)

        # Print contacts list
        for i, contact in enumerate(contacts[start:start + rows]):
            if i + start == index:
                window.addstr(4 + i, 2,
                              f"> {contact.first_name} {contact.last_name} {contact.phone_number} "
                              f"{contact.email}", curses.A_REVERSE)
            else:
                window.addstr(4 + i, 2,
                              f"  {contact.first_name} {contact.last_name} {contact.phone_number} "
                              f"{contact.email}")

        window.refresh()

    @staticmethod
    def handle_input(key, index, start, rows, list_length):
        if key == 27:  # Escape

            return "exit", index, start

        elif key == curses.KEY_DOWN:
            if index < list_length - 1:
                index += 1

                if index >= start + rows:
                    start += 1

            elif index >= list_length - 1:
                index = 0
                start = 0

        elif key == curses.KEY_UP:
            if index > 0:
                index -= 1

                if index < start:
                    start -= 1
            elif index <= 0:
                index = list_length - 1
                start = max(0, list_length - rows)

        elif key == curses.KEY_ENTER or key in [10, 13]:
            return "enter", index, start

        return "continue", index, start

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

    @staticmethod
    def display_add_contact(stdscr):
        stdscr.clear()
        stdscr.refresh()

        # Create a sub window for the contact menu
        contact_window = stdscr.subwin(10, 50, 0, 0)

        # Menu options
        enter_options = ["Name", "Surname", "Number", "Email", "Confirm"]
        selected_option = 0
        first_name, last_name, phone_number, email = '', '', '', ''

        while True:
            stdscr.clear()
            stdscr.refresh()

            contact_window.addstr(1, 1, "Add Contact:", curses.A_BOLD)
            contact_window.border(0)
            CLIFunctions.display_options(contact_window, enter_options, 3, 2, selected_option)

            contact_window.addstr(3, 14, first_name, curses.A_BOLD)
            contact_window.addstr(4, 14, last_name, curses.A_BOLD)
            contact_window.addstr(5, 14, phone_number, curses.A_BOLD)
            contact_window.addstr(6, 14, email, curses.A_BOLD)
            contact_window.refresh()

            # Wait for key
            key = contact_window.getch()

            if key == 27:  # Escape
                break  # Exit the loop and return to the main menu

            elif key == curses.KEY_DOWN:
                selected_option = (selected_option + 1) % len(enter_options)

            elif key == curses.KEY_UP:
                selected_option = (selected_option - 1) % len(enter_options)
            elif key == 10:
                if selected_option == 0:
                    first_name = CLIFunctions.input_text(stdscr, "First Name: ")

                elif selected_option == 1:
                    last_name = CLIFunctions.input_text(stdscr, "Last Name: ")

                elif selected_option == 2:
                    phone_number = CLIFunctions.input_text(stdscr, "Phone Number: ")

                elif selected_option == 3:
                    email = CLIFunctions.input_text(stdscr, "Email: ")

                elif selected_option == 4:
                    # Create a new contact and add it to the address book
                    ContactController.create_contact_and_add(first_name, last_name, phone_number, email)

                    # Confirmation message
                    CLIFunctions.display_info("Contact added successfully.")
                    break
                selected_option += 1

    @staticmethod
    def display_remove_contact(stdscr):
        stdscr.clear()
        stdscr.refresh()

        contacts = address_book.contacts
        selected_contact_index = 0
        visible_start = 0
        visible_rows = curses.LINES - 6

        # Create a sub window for the remove menu
        remove_window = stdscr.subwin(0, curses.COLS // 2 + 5, 0, 0)

        while True:
            CLIFunctions.display_list(remove_window, contacts, visible_start, visible_rows, selected_contact_index,
                                   "Remove contact:", "Press esc to leave.")

            # Wait for key
            key = remove_window.getch()

            result, selected_contact_index, visible_start = CLIFunctions.handle_input(key, selected_contact_index,
                                                                                      visible_start,
                                                                                      visible_rows, len(contacts))

            if result == "exit":
                break  # Exit the loop

            elif result == "enter":
                # Remove the selected contact
                if 0 <= selected_contact_index < len(contacts):
                    # Remove the contact from the address book
                    ContactController.remove_contact(selected_contact_index)

                    # Confirmation message
                    CLIFunctions.display_info("Contact removed successfully.")

                    selected_contact_index = max(0,
                                                 selected_contact_index - 1)  # Move the selection up after deleting
                    remove_window.clear()

    @staticmethod
    def display_contacts(stdscr, visible_start=0):
        stdscr.clear()
        stdscr.refresh()
        curses.noecho()

        # Create pretty table object
        table = PrettyTable()

        # Set table headers
        table.field_names = ["First Name", "Last Name", "Phone Number", "Email"]

        # Set table alignment
        visible_rows = curses.LINES - 4

        # Add contacts to the table
        for contact in address_book.contacts[visible_start:visible_start + visible_rows]:
            table.add_row([contact.first_name, contact.last_name, contact.phone_number, contact.email])

        # Print the table
        stdscr.addstr(0, 0, str(table))
        stdscr.refresh()

        while True:
            # Wait for key
            key = stdscr.getch()

            # Moving through the contacts list
            if key == 27:  # Escape
                break  # Exit the loop

            elif key == curses.KEY_DOWN and visible_start < len(address_book.contacts) - visible_rows:
                CLIFunctions.display_contacts(stdscr, visible_start + 1)
                break

            elif key == curses.KEY_DOWN and visible_start >= len(address_book.contacts) - visible_rows:
                CLIFunctions.display_contacts(stdscr)
                break

            elif key == curses.KEY_UP and visible_start > 0:
                CLIFunctions.display_contacts(stdscr, visible_start - 1)
                break

            elif key == curses.KEY_UP and visible_start <= 0:
                CLIFunctions.display_contacts(stdscr, len(address_book.contacts) - visible_rows)
                break

    @staticmethod
    def display_sort_contacts(stdscr):
        stdscr.clear()
        stdscr.refresh()

        sort_window = stdscr.subwin(9, 30, 9, 0)

        # Menu options
        sort_options = ["1. Name", "2. Surname", "3. Number", "4. Email"]
        selected_option = 0
        temp0, temp1, temp2, temp3 = 0, 0, 0, 0

        while True:
            stdscr.clear()
            stdscr.refresh()

            sort_window.border(0)
            sort_window.addstr(1, 1, "Sort contacts by:", curses.A_BOLD)

            CLIFunctions.display_options(sort_window, sort_options, 3, 2, selected_option)

            key = sort_window.getch()

            if key == 27:  # Escape
                break  # Exit the loop

            elif key == curses.KEY_DOWN:
                selected_option = (selected_option + 1) % len(sort_options)

            elif key == curses.KEY_UP:
                selected_option = (selected_option - 1) % len(sort_options)

            elif key == 10:  # Enter
                if selected_option == 0:
                    ContactController.sort_contacts("first_name", temp0 == 1)
                    temp0 = 1 - temp0

                elif selected_option == 1:
                    ContactController.sort_contacts("last_name", temp1 == 1)
                    temp1 = 1 - temp1

                elif selected_option == 2:
                    ContactController.sort_contacts("phone_number", temp2 == 1)
                    temp2 = 1 - temp2

                elif selected_option == 3:
                    ContactController.sort_contacts("email", temp3 == 1)
                    temp3 = 1 - temp3

                CLIFunctions.display_contacts(stdscr)

    @staticmethod
    def display_edit_contact(stdscr):
        stdscr.clear()
        stdscr.refresh()

        contacts = address_book.contacts
        selected_contact_index = 0
        visible_start = 0
        visible_rows = curses.LINES - 6

        # Create a sub window for the edit menu
        edit_window = stdscr.subwin(0, curses.COLS // 2 + 6, 0, 0)

        while True:
            CLIFunctions.display_list(edit_window, contacts, visible_start, visible_rows, selected_contact_index,
                                   "Edit contact:", "Press esc to leave.")

            # Wait for key
            key = edit_window.getch()

            result, selected_contact_index, visible_start = CLIFunctions.handle_input(key, selected_contact_index,
                                                                                      visible_start, visible_rows,
                                                                                      len(contacts))

            if result == "exit":  # Escape
                break  # Exit the loop

            elif result == "enter":  # Enter
                # Edit the selected contact
                if 0 <= selected_contact_index < len(contacts):
                    stdscr.clear()
                    stdscr.refresh()

                    edit_contact_window = stdscr.subwin(10, 50, 0, 0)  # Create a sub window

                    # Menu options
                    enter_options = ["Name", "Surname", "Number", "Email", "Confirm"]
                    selected_option = 0
                    first_name = contacts[selected_contact_index].first_name
                    last_name = contacts[selected_contact_index].last_name
                    phone_number = contacts[selected_contact_index].phone_number
                    email = contacts[selected_contact_index].email

                    while True:
                        stdscr.clear()
                        stdscr.refresh()

                        edit_contact_window.addstr(1, 1, "Edit Contact:", curses.A_BOLD)
                        edit_contact_window.border(0)
                        CLIFunctions.display_options(edit_contact_window, enter_options, 3, 2, selected_option)

                        edit_contact_window.addstr(3, 14, contacts[selected_contact_index].first_name, curses.A_BOLD)
                        edit_contact_window.addstr(4, 14, contacts[selected_contact_index].last_name, curses.A_BOLD)
                        edit_contact_window.addstr(5, 14, contacts[selected_contact_index].phone_number, curses.A_BOLD)
                        edit_contact_window.addstr(6, 14, contacts[selected_contact_index].email, curses.A_BOLD)
                        edit_contact_window.refresh()

                        key = edit_contact_window.getch()

                        if key == 27:  # Escape
                            break  # Exit the loop

                        elif key == curses.KEY_DOWN:
                            selected_option = (selected_option + 1) % len(enter_options)

                        elif key == curses.KEY_UP:
                            selected_option = (selected_option - 1) % len(enter_options)
                        elif key == 10:
                            if selected_option == 0:
                                contacts[selected_contact_index].first_name = CLIFunctions.input_text(stdscr,
                                                                                                   "First Name: ",
                                                                                                      first_name)

                            elif selected_option == 1:
                                contacts[selected_contact_index].last_name = CLIFunctions.input_text(stdscr, "Last Name: ",
                                                                                                     last_name)

                            elif selected_option == 2:
                                contacts[selected_contact_index].phone_number = CLIFunctions.input_text(stdscr,
                                                                                                     "Phone Number: ",
                                                                                                        phone_number)

                            elif selected_option == 3:
                                contacts[selected_contact_index].email = CLIFunctions.input_text(stdscr, "Email: ", email)

                            elif selected_option == 4:
                                # Confirmation changes

                                message = "Contact edited successfully."
                                # Confirmation message
                                CLIFunctions.display_info(message)
                                break

                            selected_option += 1

    @staticmethod
    def clear_contacts_list():
        # Clear the contacts list
        ContactController.clear_contacts()
        message = "Contacts cleared successfully."
        CLIFunctions.display_info(message)

    @staticmethod
    def display_recycle_bin(stdscr):
        stdscr.clear()
        stdscr.refresh()

        contacts = address_book.removed_contacts
        selected_contact_index = 0
        visible_start = 0
        visible_rows = curses.LINES - 6

        # Create a sub window for the recycle bin menu
        recycle_bin_window = stdscr.subwin(0, curses.COLS // 2 + 4, 0, 0)

        while True:
            CLIFunctions.display_list(recycle_bin_window, contacts, visible_start, visible_rows, selected_contact_index,
                                   "Recycle bin:", "Press esc to leave.")

            # Wait for key
            key = recycle_bin_window.getch()

            result, selected_contact_index, visible_start = CLIFunctions.handle_input(key, selected_contact_index,
                                                                                      visible_start, visible_rows,
                                                                                      len(contacts))

            if result == "exit":
                break

            elif result == "enter":
                # Restore the selected contact
                if 0 <= selected_contact_index < len(contacts):
                    # Restore the contact to the address book
                    address_book.contacts.append(address_book.removed_contacts[selected_contact_index])
                    address_book.removed_contacts.pop(selected_contact_index)

                    # Confirmation message
                    CLIFunctions.display_info("Contact restored successfully.")

                    selected_contact_index = max(0,
                                                 selected_contact_index - 1)

    @staticmethod
    def display_exit(stdscr):
        stdscr.clear()
        stdscr.refresh()

        # Menu options
        exit_options = ["1. Save contacts", "2. Without saving", "3. Back"]
        selected_option = 0

        screen_height, screen_width = stdscr.getmaxyx()

        # put window in the center
        exit_window_height, exit_window_width = 6, 30
        exit_window_y = (screen_height - exit_window_height) // 2
        exit_window_x = (screen_width - exit_window_width) // 2

        exit_window = stdscr.subwin(exit_window_height, exit_window_width, exit_window_y, exit_window_x)
        exit_window.border(0)

        # Print message
        exit_window.addstr(1, 10, "Exit options:", curses.A_BOLD)

        while True:
            # Print exit options
            CLIFunctions.display_options(exit_window, exit_options, 2, 2, selected_option)

            exit_window.refresh()
            key = exit_window.getch()

            if key == curses.KEY_DOWN:
                selected_option = (selected_option + 1) % len(exit_options)
            elif key == curses.KEY_UP:
                selected_option = (selected_option - 1) % len(exit_options)
            elif key == 10:  # Enter
                if selected_option == 0:
                    # Save contacts
                    FileController.save_contacts_to_file('contacts.txt', address_book.contacts)
                    logger.log_info("Application closed.\n")
                    curses.endwin()
                    sys.exit(0)  # Leave the script
                elif selected_option == 1:
                    logger.log_info("Application closed.\n")
                    curses.endwin()
                    sys.exit(0)  # Leave the script
                elif selected_option == 2:
                    # Back
                    logger.log_info("Back to main menu.")
                    break

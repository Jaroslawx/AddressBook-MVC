from utils.Log import logger
from Controllers.FileController import file_controller
from Models.Trivia import trivia
from Models.AddressBook import address_book
from Models.Contact import Contact
from Views.Textual.Interface import textual_view

import curses


def main(stdscr):
    logger.log_info("Application started.")

    contact0 = Contact("Marek", "Groove", "321-654-0987", "marek.groove@example.com")
    contact1 = Contact("Jan", "Kowalski", "123-456-7890", "jan.kowalski@example.com")
    contact2 = Contact("Anna", "Nowak", "987-654-3210", "anna.nowak@example.com")
    contact3 = Contact("Piotr", "Nowicki", "555-123-4567", "piotr.nowicki@example.com")
    address_book.add_contact(contact0)
    address_book.add_contact(contact1)
    address_book.add_contact(contact2)
    address_book.add_contact(contact3)

    # Add more contacts for testing purposes
    for i in range(35):
        address_book.contacts.append(Contact(f"First{i}", f"Last{i}", f"Phone{i}", f"Email{i}@example.com"))

    if textual_view.display_start(stdscr) == 1:
        while True:
            textual_view.display_menu(stdscr)


curses.wrapper(main)

if __name__ == '__main__':
    main(stdscr=curses.initscr())

# TODO:
# - keep the place you left in the menu after returning

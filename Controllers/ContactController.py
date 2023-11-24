from utils.Log import logger
from Models.Contact import Contact
from Models.AddressBook import address_book


class ContactController:
    @staticmethod
    def create_contact_and_add(first_name, last_name, phone, email):
        new_contact = Contact(first_name, last_name, phone, email)
        address_book.add_contact(new_contact)
        logger.log_info(f"Contact {new_contact} added to the list.")

    @staticmethod
    def remove_contact(index):
        address_book.contacts.pop(index)
        logger.log_info(f"Contact deleted from the list.")

    @staticmethod
    def clear_contacts():
        address_book.contacts.clear()
        logger.log_info(f"Contacts cleared from the list.")
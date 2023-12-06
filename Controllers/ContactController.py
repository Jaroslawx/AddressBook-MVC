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
        address_book.removed_contacts.append(address_book.contacts[index])
        address_book.contacts.pop(index)
        logger.log_info(f"Contact deleted from the list and added to the recycle bin.")

    @staticmethod
    def restore_contact(index):
        address_book.contacts.append(address_book.removed_contacts[index])
        address_book.removed_contacts.pop(index)
        logger.log_info(f"Contact restored from the recycle bin.")

    @staticmethod
    def sort_contacts(option, reverse_flag):
        def sorting_key(contact):  # returns the value of the attribute to be sorted
            return getattr(contact, option)

        address_book.contacts.sort(key=sorting_key, reverse=reverse_flag)
        logger.log_info(f"Contacts sorted by {option} in {'descending' if reverse_flag else 'ascending'} order.")

    @staticmethod
    def clear_contacts():
        address_book.contacts.clear()
        address_book.removed_contacts.clear()
        logger.log_info(f"Contacts cleared from the list and recycle bin.")

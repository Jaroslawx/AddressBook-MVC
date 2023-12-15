from utils.Log import logger
from Models.Contact import Contact
from Models.AddressBook import address_book


class ContactController:
    @staticmethod
    def create_contact_and_add(first_name, last_name, phone, email):
        new_contact = Contact(first_name, last_name, phone, email)
        address_book.add_contact(new_contact)
        address_book.backup_contacts.append(new_contact)
        logger.log_info(f"Contact {new_contact} added to the list.")

    @staticmethod
    def remove_contact(index):
        address_book.removed_contacts.append(address_book.contacts[index])
        address_book.contacts.pop(index)
        logger.log_info(f"Contact deleted from the list and added to the recycle bin.")

    @staticmethod
    def search_contact(name="", surname="", phone="", email=""):
        # Create search results list
        results = []

        # Iterate over all contacts
        for contact in address_book.contacts:
            # Check if the contact matches the search criteria
            if (not name or name.lower() in contact.first_name.lower()) and \
                    (not surname or surname.lower() in contact.last_name.lower()) and \
                    (not phone or str(phone) in str(contact.phone_number)) and \
                    (not email or email.lower() in contact.email.lower()):
                # Add the contact to the results list
                results.append(contact)

        return results

    @staticmethod
    def restore_contact(index):
        address_book.contacts.append(address_book.removed_contacts[index])
        address_book.backup_contacts.append(address_book.removed_contacts[index])
        address_book.removed_contacts.pop(index)
        logger.log_info(f"Contact restored from the recycle bin.")

    @staticmethod
    def sort_contacts(attribute, reverse_flag):
        def sorting_key(contact):  # returns the value of the attribute to be sorted
            return getattr(contact, attribute)

        address_book.contacts.sort(key=sorting_key, reverse=reverse_flag)
        logger.log_info(f"Contacts sorted by {attribute} in {'descending' if reverse_flag else 'ascending'} order.")

    @staticmethod
    def clear_contacts():
        address_book.contacts.clear()
        address_book.removed_contacts.clear()
        logger.log_info(f"Contacts cleared from the list and recycle bin.")

    @staticmethod
    def synchronize_contacts():
        # Remove contacts from backup_contacts
        for removed_contact in address_book.removed_contacts:
            if removed_contact in address_book.backup_contacts:
                address_book.backup_contacts.remove(removed_contact)

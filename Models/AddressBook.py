class AddressBook:
    def __init__(self):
        self.contacts = []
        self.backup_contacts = []
        self.removed_contacts = []

    def add_contact(self, contact):
        self.contacts.append(contact)
        self.backup_contacts.append(contact)

    def add_removed_contact(self, contact):
        self.removed_contacts.append(contact)


address_book = AddressBook()

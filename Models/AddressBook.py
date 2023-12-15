class AddressBook:
    def __init__(self):
        self.contacts = []
        self.unmatched_contacts = []
        self.removed_contacts = []

    def add_contact(self, contact):
        self.contacts.append(contact)

    def add_removed_contact(self, contact):
        self.removed_contacts.append(contact)


address_book = AddressBook()

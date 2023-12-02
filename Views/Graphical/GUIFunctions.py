import sys


class GUIFunctions:
    def __init__(self, gui_root):
        self.root = gui_root

    def add_contact(self):
        # Handle adding a contact
        pass

    def remove_contact(self):
        # Handle removing a contact
        pass

    def display_contacts(self):
        # Handle displaying contacts
        pass

    def sort_contacts(self):
        # Handle sorting contacts
        pass

    def edit_contact(self):
        # Handle editing a contact
        pass

    def clear_contacts(self):
        # Handle clearing contacts
        pass

    def recycle_bin(self):
        # Handle the recycle bin
        pass

    def exit_program(self):
        # Handle exiting the program
        self.root.destroy()
        sys.exit(0)

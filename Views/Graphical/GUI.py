from utils.Log import logger
from Controllers.FileController import FileController
from Models.Trivia import trivia
from Models.AddressBook import address_book
from Views.Graphical.GUIFunctions import GUIFunctions

import tkinter as tk
import threading
import time
import datetime


class GUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("1000x700")
        self.root.config(bg="green")
        self.root.resizable(False, False)
        self.root.title("Address Book")

        # Create menu bar
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        # Create menu "File"
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)

        # Add options to menu "File"
        file_menu.add_command(label="Load contacts from", command=FileController.load_contacts_and_add)
        file_menu.add_command(label="Save contacts to", command=FileController.save_contacts_to_file)

        buttons = ["Add contact", "Remove contact", "Display contacts", "Sort contacts",
                   "Edit contact", "Clear contacts", "Recycle bin", "Exit"]

        # Create buttons
        for button_label in buttons:
            button = tk.Button(self.root, text=button_label,
                               command=lambda label=button_label: self.button_handler(label))
            button.pack(pady=5)

    @staticmethod
    def button_handler(label):
        # Map button labels to corresponding methods in GUIFunctions
        button_mapping = {
            "add_contact": gui_functions.add_contact,
            "remove_contact": gui_functions.remove_contact,
            "display_contacts": gui_functions.display_contacts,
            "sort_contacts": gui_functions.sort_contacts,
            "edit_contact": gui_functions.edit_contact,
            "clear_contacts": gui_functions.clear_contacts,
            "recycle_bin": gui_functions.recycle_bin,
            "exit": gui_functions.exit_program,
        }

        # Get the corresponding method for the given label and call it
        button_mapping.get(label.lower().replace(" ", "_"), lambda: None)()

    def start_gui(self):
        # Start main GUI loop
        self.root.mainloop()


graphical_view = GUI()
gui_functions = GUIFunctions(graphical_view.root)

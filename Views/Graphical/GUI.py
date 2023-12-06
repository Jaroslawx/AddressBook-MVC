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
        self.master = tk.Tk()
        self.master.geometry("1000x700")
        self.master.config(bg="green")
        self.master.resizable(False, False)
        self.master.title("Address Book")

        # Create menu bar
        menubar = tk.Menu(self.master)
        self.master.config(menu=menubar)

        # Create menu "File"
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)

        # Add options to menu "File"
        file_menu.add_command(label="Load contacts from", command=FileController.load_contacts_and_add)
        file_menu.add_command(label="Save contacts to", command=FileController.save_contacts_to_file)

        # # Create menu "View"
        # file_menu = tk.Menu(menubar, tearoff=0)
        # menubar.add_cascade(label="View", menu=file_menu)
        #
        # # Add options to menu "File"
        # file_menu.add_command(label="Hide date", command=FileController.load_contacts_and_add)
        # file_menu.add_command(label="Hide trivia", command=FileController.save_contacts_to_file)

        # Create a frame for date display
        date_frame = tk.Frame(self.master, bg="green")
        date_frame.pack(side=tk.RIGHT, anchor=tk.NE, padx=10, pady=10)

        # Label for displaying date
        self.date_label = tk.Label(date_frame, text="", font=("Helvetica", 12), bg="green", fg="white")
        self.date_label.pack()

        # Create buttons
        button_frame = tk.Frame(self.master, bg="green")
        button_frame.pack(anchor=tk.NW, padx=5, pady=5)

        buttons = ["Add contact", "Remove contact", "Display contacts", "Sort contacts",
                   "Edit contact", "Clear contacts", "Recycle bin", "Exit"]

        for button_label in buttons:
            button = tk.Button(button_frame, text=button_label,
                               command=lambda label=button_label: self.button_handler(label), width=20, height=2)
            button.pack(side=tk.TOP, pady=5)

        # Display date
        self.update_date()

        # Create a frame for displaying a random fact
        fact_frame = tk.Frame(self.master, bg="green")
        fact_frame.pack(side=tk.BOTTOM, anchor=tk.SW, padx=10, pady=10)

        # Label for displaying a random fact
        self.fact_label = tk.Label(fact_frame, text="", font=("Helvetica", 12), bg="green", fg="white", wraplength=600)
        self.fact_label.pack()

        # Display a random fact
        self.update_random_fact()

        GUIFunctions.center_window(self.master)

    def update_date(self):
        # Update the date label
        current_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.date_label.config(text=f"Date: {current_date}")
        self.master.after(1000, self.update_date)  # Schedule the next update after 1000 milliseconds (1 second)

    def update_random_fact(self):
        # Update the fact label with a random fact
        random_fact = trivia.get_random_trivia()
        self.fact_label.config(text=f"{random_fact}")

        # Schedule the next update after 10 seconds
        self.master.after(10000, self.update_random_fact)

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
        logger.log_info("Starting GUI...")
        # Start main GUI loop
        self.master.mainloop()


graphical_view = GUI()
gui_functions = GUIFunctions(graphical_view.master)

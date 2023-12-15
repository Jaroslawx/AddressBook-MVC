from utils.Log import logger
from Controllers.FileController import FileController
from Models.Trivia import trivia
# from Models.AddressBook import address_book
from Views.Graphical.GUIFunctions import GUIFunctions

import tkinter as tk
import datetime


class GUI:
    def __init__(self):
        self.master = tk.Tk()
        self.master.geometry("1000x700")
        self.master.config(bg="#FFF5E1")
        self.master.resizable(False, False)
        self.master.title("Address Book")
        self.master.iconbitmap("assets/icon.ico")

        # Create menu bar
        menubar = tk.Menu(self.master)
        self.master.config(menu=menubar)

        # Create menu "File"
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)

        # Add options to menu "File"
        file_menu.add_command(label="Load contacts from", command=self.load_contacts_from_file)
        file_menu.add_command(label="Save contacts to", command=FileController.save_contacts_to_file)

        # Label for displaying date
        self.date_label = tk.Label(self.master, text="", font=("Helvetica", 12), bg="#FFF5E1", fg="black")
        self.date_label.pack(anchor=tk.SW, padx=10, pady=10)

        # Display date
        self.update_date()

        # Create a frame for the center area
        middle_frame = tk.Frame(self.master, bg="white", bd=5, relief=tk.GROOVE)
        middle_frame.pack(expand=True, fill="both", padx=5, pady=5)

        # Create buttons
        button_frame = tk.Frame(middle_frame, bg="white", bd=5, relief=tk.SUNKEN)
        button_frame.pack(side=tk.LEFT, padx=5, pady=5)

        buttons = ["Add contact", "Sort contacts", "Clear contacts", "Recycle bin", "Exit"]

        for button_label in buttons:
            button = tk.Button(button_frame, text=button_label,
                               command=lambda label=button_label: self.button_handler(label), width=20, height=2)
            button.pack(side=tk.TOP, pady=5)

        # Create a frame for the table
        super_table_frame = tk.Frame(middle_frame, bg="white", bd=5, relief=tk.GROOVE)
        super_table_frame.pack(side=tk.LEFT, expand=True, fill="both", padx=5, pady=5)

        # Create an instance of GUIFunctions
        self.gui_functions = GUIFunctions(self.master, super_table_frame)

        # Call super_table_display using the instance
        self.gui_functions.super_table_display()

        # Label for "Fun Fact" heading
        self.fun_fact_heading = tk.Label(self.master, text="Fun Fact:", font=("Helvetica", 12, "bold"), bg="#FFF5E1",
                                         fg="black")
        self.fun_fact_heading.pack(side=tk.TOP, anchor=tk.CENTER, padx=10, pady=10)

        # Label for displaying a random fact
        self.fun_fact_label = tk.Label(self.master, text="", font=("Helvetica", 11), bg="#FFF5E1", fg="black",
                                       wraplength=1000)
        self.fun_fact_label.pack(side=tk.TOP, anchor=tk.CENTER, padx=10, pady=10)

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
        self.fun_fact_label.config(text=f"{random_fact}")

        # Schedule the next update after 10 seconds
        self.master.after(10000, self.update_random_fact)

    def button_handler(self, label):
        # Map button labels to corresponding methods in GUIFunctions
        button_mapping = {
            "add_contact": self.gui_functions.add_contact,
            "sort_contacts": self.gui_functions.sort_contacts,
            "clear_contacts": self.gui_functions.clear_contacts,
            "recycle_bin": self.gui_functions.recycle_bin,
            "exit": self.gui_functions.exit_program,
        }

        # Get the corresponding method for the given label and call it
        button_mapping.get(label.lower().replace(" ", "_"), lambda: None)()

        # Update the treeview
        self.gui_functions.update_treeview()

    def load_contacts_from_file(self):
        # Load contacts from file
        FileController.load_contacts_and_add()

        # Update the treeview
        self.gui_functions.update_treeview()

    def start_gui(self):
        logger.log_info("Starting GUI...")

        # Start main GUI loop
        self.master.mainloop()

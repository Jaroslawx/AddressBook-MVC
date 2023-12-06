from utils.Log import logger
from Models.AddressBook import address_book
from Controllers.ContactController import ContactController

import tkinter as tk
from tkinter import ttk
import sys


class GUIFunctions:
    def __init__(self, master):
        self.root = master

    def add_contact(self):
        # Handle adding a contact
        subwindow = tk.Toplevel(self.root)
        subwindow.title("Add Contact")

        # Labels and Entry widgets for user input
        first_name_label = tk.Label(subwindow, text="First Name:")
        first_name_label.grid(row=0, column=0, padx=10, pady=5, sticky=tk.E)
        first_name_entry = tk.Entry(subwindow)
        first_name_entry.grid(row=0, column=1, padx=10, pady=5)

        last_name_label = tk.Label(subwindow, text="Last Name:")
        last_name_label.grid(row=1, column=0, padx=10, pady=5, sticky=tk.E)
        last_name_entry = tk.Entry(subwindow)
        last_name_entry.grid(row=1, column=1, padx=10, pady=5)

        phone_number_label = tk.Label(subwindow, text="Phone Number:")
        phone_number_label.grid(row=2, column=0, padx=10, pady=5, sticky=tk.E)
        phone_number_entry = tk.Entry(subwindow)
        phone_number_entry.grid(row=2, column=1, padx=10, pady=5)

        email_label = tk.Label(subwindow, text="Email:")
        email_label.grid(row=3, column=0, padx=10, pady=5, sticky=tk.E)
        email_entry = tk.Entry(subwindow)
        email_entry.grid(row=3, column=1, padx=10, pady=5)

        # Button to confirm contact addition
        add_button = tk.Button(subwindow, text="Add", command=lambda: self.confirm_add_contact(
            subwindow, first_name_entry.get(), last_name_entry.get(), phone_number_entry.get(), email_entry.get()))
        add_button.grid(row=4, columnspan=2, pady=10)

    @staticmethod
    def confirm_add_contact(subwin, first_name, last_name, phone_number, email):
        # Handle confirming the addition of a contact
        ContactController.create_contact_and_add(
            first_name, last_name, phone_number, email)

        # Close the subwindow after adding the contact
        subwin.destroy()

    def remove_contact(self):
        # Handle removing a contact
        pass

    def display_contacts(self):
        # Handle displaying contacts
        self.display_contacts_window()

    def display_contacts_window(self):
        contacts_window = tk.Toplevel(self.root)
        contacts_window.title("Display Contacts")
        contacts_window.geometry("700x600")

        # Create Treeview widget
        tree = ttk.Treeview(contacts_window)
        tree["columns"] = ("First Name", "Last Name", "Phone Number", "Email")

        # Define column headings
        tree.heading("#0", text="")
        tree.column("#0", anchor=tk.W, width=0)

        tree.heading("First Name", text="First Name")
        tree.column("First Name", anchor=tk.W, width=100)

        tree.heading("Last Name", text="Last Name")
        tree.column("Last Name", anchor=tk.W, width=100)

        tree.heading("Phone Number", text="Phone Number")
        tree.column("Phone Number", anchor=tk.W, width=120)

        tree.heading("Email", text="Email")
        tree.column("Email", anchor=tk.W, width=150)

        # Insert actual data from the AddressBook
        for i, contact in enumerate(address_book.contacts, 1):
            tree.insert("", "end", values=(contact.first_name, contact.last_name,
                                           contact.phone_number, contact.email))

        # Add scrollbar
        scrollbar = ttk.Scrollbar(contacts_window, orient="vertical", command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        # Pack the Treeview widget
        tree.pack(expand=True, fill="both")

        # Center the window on the screen
        contacts_window.update_idletasks()
        width = contacts_window.winfo_width()
        height = contacts_window.winfo_height()
        x = contacts_window.winfo_screenwidth() - width
        y = 0
        contacts_window.geometry(f"{width}x{height}+{x}+{y}")

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

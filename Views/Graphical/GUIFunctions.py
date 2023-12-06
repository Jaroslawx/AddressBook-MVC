from utils.Log import logger
from Models.AddressBook import address_book
from Controllers.ContactController import ContactController

import tkinter as tk
from tkinter import ttk, messagebox
import sys


class GUIFunctions:
    def __init__(self, master):
        self.root = master

    @staticmethod
    def tree_contacts(window, contact_list):
        # Create Treeview widget
        tree = ttk.Treeview(window)
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
        for i, contact in enumerate(contact_list, 1):
            tree.insert("", "end", values=(contact.first_name, contact.last_name,
                                           contact.phone_number, contact.email))

        # Configure scrollbar
        scrollbar = ttk.Scrollbar(window, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        # Pack the Treeview widget
        tree.pack(expand=True, fill="both")

    @staticmethod
    def center_window(window):
        # Set the position of the window to the center of the screen
        window.update_idletasks()

        width = window.winfo_width()
        height = window.winfo_height()
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2

        window.geometry(f"{width}x{height}+{x}+{y}")

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
        def remove_selected_contact():
            selected_index = contacts_listbox.curselection()
            if selected_index:
                # Confirm removal
                confirmation = messagebox.askyesno("Confirmation", "Are you sure you want to remove this contact?")
                if confirmation:
                    # Remove the contact from the address book
                    ContactController.remove_contact(selected_index[0])
                    # Update the contacts listbox
                    update_contacts_listbox()
                    messagebox.showinfo("Success", "Contact removed successfully.")
            else:
                messagebox.showwarning("Warning", "Please select a contact to remove.")

        def update_contacts_listbox():
            # Clear the current contents of the listbox
            contacts_listbox.delete(0, tk.END)
            # Populate the Listbox with contact names
            for contact in address_book.contacts:
                contacts_listbox.insert(tk.END, f"{contact.first_name} {contact.last_name} {contact.phone_number} "
                                                f"{contact.email}")

        # Display a Toplevel window to show the list of contacts
        remove_window = tk.Toplevel(self.root)
        remove_window.title("Remove Contact")
        remove_window.geometry("500x400")

        # Create a Listbox to display contacts
        contacts_listbox = tk.Listbox(remove_window, selectmode=tk.SINGLE, width=90, height=20)
        contacts_listbox.pack(padx=10, pady=10)

        # Populate the Listbox with contact names
        for contact in address_book.contacts:
            contacts_listbox.insert(tk.END, f"{contact.first_name} {contact.last_name} {contact.phone_number} "
                                            f"{contact.email}")

        # Add a button to remove the selected contact
        remove_button = tk.Button(remove_window, text="Remove Selected Contact", command=remove_selected_contact)
        remove_button.pack(pady=10)

        # Add a button to exit the loop and close the window
        exit_button = tk.Button(remove_window, text="Exit", command=remove_window.destroy)
        exit_button.pack(pady=10)

        # Center the window on the screen
        self.center_window(remove_window)

        # Start the main loop for the Toplevel window
        remove_window.mainloop()

    def display_contacts(self):
        contacts_window = tk.Toplevel(self.root)
        contacts_window.title("Display Contacts")
        contacts_window.geometry("700x600")

        GUIFunctions.tree_contacts(contacts_window, address_book.contacts)

        GUIFunctions.center_window(contacts_window)

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
        recycle_bin_window = tk.Toplevel(self.root)
        recycle_bin_window.title("Display Contacts")
        recycle_bin_window.geometry("700x500")

        GUIFunctions.tree_contacts(recycle_bin_window, address_book.removed_contacts)

        GUIFunctions.center_window(recycle_bin_window)

    def exit_program(self):
        # Handle exiting the program
        self.root.destroy()
        sys.exit(0)

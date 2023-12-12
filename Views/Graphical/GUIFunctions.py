from utils.Log import logger
from Models.AddressBook import address_book
from Controllers.ContactController import ContactController

import tkinter as tk
from tkinter import ttk, messagebox
import sys


class GUIFunctions:
    def __init__(self, master, super_table_frame):
        self.root = master
        self.super_tree = None
        self.super_table_frame = super_table_frame

    @staticmethod
    def tree_contacts(window, contact_list):
        logger.log_info("Displaying contacts in a Treeview widget.")
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
        logger.log_info("Centering window on screen.")
        # Set the position of the window to the center of the screen
        window.update_idletasks()

        width = window.winfo_width()
        height = window.winfo_height()
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2

        window.geometry(f"{width}x{height}+{x}+{y}")

    def create_contacts_listbox(self, name="Window"):
        # Display a Toplevel window to show the list of contacts
        window = tk.Toplevel(self.root)
        window.title(name)
        window.geometry("500x400")

        # Create a Listbox to display contacts
        listbox = tk.Listbox(window, selectmode=tk.SINGLE, width=90, height=20)
        listbox.pack(padx=10, pady=10)

        # Populate the Listbox with contact names
        for contact in address_book.contacts:
            listbox.insert(tk.END, f"{contact.first_name} {contact.last_name} {contact.phone_number} "
                                   f"{contact.email}")

        return window, listbox

    @staticmethod
    def create_exit_button(window, side=tk.LEFT, x=10, y=10):
        # Add a button to exit the loop and close the window
        exit_button = tk.Button(window, text="Exit", command=window.destroy)
        exit_button.pack(side=side, padx=x, pady=y)

    def add_contact(self):
        logger.log_info("Adding a contact.")
        # Handle adding a contact
        add_window = tk.Toplevel(self.root)
        add_window.title("Add Contact")

        # Labels and Entry widgets for user input
        first_name_label = tk.Label(add_window, text="First Name:")
        first_name_label.grid(row=0, column=0, padx=10, pady=5, sticky=tk.E)
        first_name_entry = tk.Entry(add_window)
        first_name_entry.grid(row=0, column=1, padx=10, pady=5)

        last_name_label = tk.Label(add_window, text="Last Name:")
        last_name_label.grid(row=1, column=0, padx=10, pady=5, sticky=tk.E)
        last_name_entry = tk.Entry(add_window)
        last_name_entry.grid(row=1, column=1, padx=10, pady=5)

        phone_number_label = tk.Label(add_window, text="Phone Number:")
        phone_number_label.grid(row=2, column=0, padx=10, pady=5, sticky=tk.E)
        phone_number_entry = tk.Entry(add_window)
        phone_number_entry.grid(row=2, column=1, padx=10, pady=5)

        email_label = tk.Label(add_window, text="Email:")
        email_label.grid(row=3, column=0, padx=10, pady=5, sticky=tk.E)
        email_entry = tk.Entry(add_window)
        email_entry.grid(row=3, column=1, padx=10, pady=5)

        # Button to confirm contact addition
        add_button = tk.Button(add_window, text="Add", command=lambda: self.confirm_add_contact(
            add_window, first_name_entry.get(), last_name_entry.get(), phone_number_entry.get(), email_entry.get()))
        add_button.grid(row=4, columnspan=2, pady=10)

    def confirm_add_contact(self, window, first_name, last_name, phone_number, email):
        # Handle confirming the addition of a contact
        ContactController.create_contact_and_add(
            first_name, last_name, phone_number, email)

        # Update the treeview
        self.update_treeview()

        # Close the window after adding the contact
        window.destroy()

    def remove_contact(self):
        logger.log_info("Removing a contact.")

        # Handle removing a contact
        remove_window, contacts_listbox = self.create_contacts_listbox("Remove Contact")

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
            for c in address_book.contacts:
                contacts_listbox.insert(tk.END, f"{c.first_name} {c.last_name} {c.phone_number} "
                                                f"{c.email}")
            # Update the treeview
            self.update_treeview()

        # Add a button to remove the selected contact
        remove_button = tk.Button(remove_window, text="Remove Contact", command=remove_selected_contact)
        remove_button.pack(side=tk.LEFT, padx=5, pady=10)

        self.create_exit_button(remove_window, tk.LEFT, 5, 10)

        # Center the window on the screen
        self.center_window(remove_window)

        # Start the main loop for the Toplevel window
        remove_window.mainloop()

    def display_contacts(self):
        logger.log_info("Displaying contacts.")
        # Handle displaying contacts
        display_window = tk.Toplevel(self.root)
        display_window.title("Display Contacts")
        display_window.geometry("700x600")

        GUIFunctions.tree_contacts(display_window, address_book.contacts)

        GUIFunctions.center_window(display_window)

    def sort_contacts(self):
        # Display a Toplevel window for sorting contacts
        sort_window = tk.Toplevel(self.root)
        sort_window.title("Sort Contacts")
        sort_window.geometry("300x200")

        # Function to handle sorting contacts
        def temp_sort(heading, reverse_flag):
            ContactController.sort_contacts(heading, reverse_flag)
            messagebox.showinfo("Success",
                                f"Contacts sorted by {label_mapping[heading]} in "
                                f"{'descending' if reverse_flag else 'ascending'} order.")

            # Update the treeview
            self.update_treeview()

        # Create labels and buttons for sorting
        sort_labels = ["Name", "Surname", "Number", "Email"]
        pattern = ["first_name", "last_name", "phone_number", "email"]
        # Mapping option to label
        label_mapping = {"first_name": "Name", "last_name": "Surname", "phone_number": "Number", "email": "Email"}

        for label, option in zip(sort_labels, pattern):
            label_frame = tk.Frame(sort_window)
            label_frame.pack(pady=5)

            label_text = tk.Label(label_frame, text=f"By {label}")
            label_text.pack(side=tk.LEFT)

            asc_button = tk.Button(label_frame, text="Ascending", command=lambda opt=option: temp_sort(opt, False))
            asc_button.pack(side=tk.LEFT, padx=5)

            desc_button = tk.Button(label_frame, text="Descending", command=lambda opt=option: temp_sort(opt, True))
            desc_button.pack(side=tk.LEFT)

        # Add a button to exit the loop and close the window
        exit_button = tk.Button(sort_window, text="Exit", command=sort_window.destroy)
        exit_button.pack(pady=10)

        # Center the window on the screen
        GUIFunctions.center_window(sort_window)

        # Start the main loop for the Toplevel window
        sort_window.mainloop()

    def edit_contact(self):
        logger.log_info("Editing a contact.")

        # Handle editing a contact
        edit_window, contacts_listbox = self.create_contacts_listbox("Edit Contact")

        # Function to handle editing a contact
        def edit_selected_contact():
            selected_index = contacts_listbox.curselection()
            if selected_index:
                # Get the selected contact
                selected_contact = address_book.contacts[selected_index[0]]

                # Create a Toplevel window for editing
                edit_contact_window = tk.Toplevel(edit_window)
                edit_contact_window.title("Edit Contact")

                # Display the old and new values
                tk.Label(edit_contact_window, text="Old Value:").grid(row=0, column=0)
                tk.Label(edit_contact_window, text="New Value:").grid(row=0, column=1)

                # Display old values
                tk.Label(edit_contact_window, text=f"First Name: {selected_contact.first_name}").grid(row=1, column=0)
                tk.Label(edit_contact_window, text=f"Last Name: {selected_contact.last_name}").grid(row=2, column=0)
                tk.Label(edit_contact_window, text=f"Phone Number: {selected_contact.phone_number}").grid(row=3,
                                                                                                          column=0)
                tk.Label(edit_contact_window, text=f"Email: {selected_contact.email}").grid(row=4, column=0)

                # Entry widgets for new values
                new_first_name_entry = tk.Entry(edit_contact_window)
                new_last_name_entry = tk.Entry(edit_contact_window)
                new_phone_number_entry = tk.Entry(edit_contact_window)
                new_email_entry = tk.Entry(edit_contact_window)

                new_first_name_entry.grid(row=1, column=1)
                new_last_name_entry.grid(row=2, column=1)
                new_phone_number_entry.grid(row=3, column=1)
                new_email_entry.grid(row=4, column=1)

                # Function to handle updating the contact
                def update_contact():
                    # Get new values
                    new_first_name = new_first_name_entry.get()
                    new_last_name = new_last_name_entry.get()
                    new_phone_number = new_phone_number_entry.get()
                    new_email = new_email_entry.get()

                    # Update the contact
                    selected_contact.first_name = new_first_name if new_first_name \
                        else selected_contact.first_name
                    selected_contact.last_name = new_last_name if new_last_name \
                        else selected_contact.last_name
                    selected_contact.phone_number = new_phone_number if new_phone_number \
                        else selected_contact.phone_number
                    selected_contact.email = new_email if new_email \
                        else selected_contact.email

                    # Update the Listbox
                    contacts_listbox.delete(selected_index[0])
                    contacts_listbox.insert(selected_index[0], f"{selected_contact.first_name} "
                                                               f"{selected_contact.last_name} "
                                                               f"{selected_contact.phone_number} "
                                                               f"{selected_contact.email}")

                    messagebox.showinfo("Success", "Contact updated successfully.")

                    # Update the treeview
                    self.update_treeview()

                    edit_contact_window.destroy()

                # Add a button to update the contact
                update_button = tk.Button(edit_contact_window, text="Update Contact", command=update_contact)
                update_button.grid(row=5, column=0, columnspan=2, pady=10)

            else:
                messagebox.showwarning("Warning", "Please select a contact to edit.")

        # Add a button to edit the selected contact
        edit_button = tk.Button(edit_window, text="Edit Contact", command=edit_selected_contact)
        edit_button.pack(pady=10)

        # Add a button to exit the loop and close the window
        exit_button = tk.Button(edit_window, text="Exit", command=edit_window.destroy)
        exit_button.pack(pady=10)

        # Center the window on the screen
        GUIFunctions.center_window(edit_window)

        # Start the main loop for the Toplevel window
        edit_window.mainloop()

    def clear_contacts(self):
        logger.log_info("Clearing contacts.")
        # Handle clearing contacts
        ContactController.clear_contacts()

        # Update the treeview
        self.update_treeview()

    def recycle_bin(self):
        # Function to handle restoring a contact from the recycle bin
        def restore_selected_contact():
            selected_index = listbox.curselection()
            if selected_index:
                # Confirm restoration
                confirmation = messagebox.askyesno("Confirmation", "Are you sure you want to restore this contact?")
                if confirmation:
                    # Restore the contact to the main address book
                    ContactController.restore_contact(selected_index[0])
                    # Update the recycle bin
                    update_recycle_bin()
                    messagebox.showinfo("Success", "Contact restored successfully.")
            else:
                messagebox.showwarning("Warning", "Please select a contact to restore.")

        # Function to update the recycle bin after restoring a contact
        def update_recycle_bin():
            # Clear the current contents of the Listbox
            listbox.delete(0, tk.END)

            # Populate the Listbox with contact names
            for c in address_book.removed_contacts:
                listbox.insert(tk.END,
                               f"{c.first_name} {c.last_name} {c.phone_number} {c.email}")

            # Update the treeview
            self.update_treeview()

        # Display a Toplevel window to show the list of contacts
        restore_window = tk.Toplevel(self.root)
        restore_window.title("Recycle Bin")
        restore_window.geometry("500x400")

        # Create Listbox widget for the recycle bin
        listbox = tk.Listbox(restore_window, selectmode=tk.SINGLE, width=90, height=20)
        listbox.pack(padx=10, pady=10)

        # Populate the Listbox with contact names from the removed contacts
        for contact in address_book.removed_contacts:
            listbox.insert(tk.END, f"{contact.first_name} {contact.last_name} {contact.phone_number} {contact.email}")

        # Add a button to remove the selected contact
        restore_button = tk.Button(restore_window, text="Restore Contact", command=restore_selected_contact)
        restore_button.pack(side=tk.LEFT, padx=5, pady=10)

        # Add a button to exit the loop and close the window
        exit_button = tk.Button(restore_window, text="Exit", command=restore_window.destroy)
        exit_button.pack(side=tk.LEFT, padx=5, pady=10)

        # Center the window on the screen
        GUIFunctions.center_window(restore_window)

        # Start the main loop for the Toplevel window
        restore_window.mainloop()

    def exit_program(self):
        logger.log_info("Application closed.")
        # Handle exiting the program
        self.root.destroy()
        sys.exit(0)

    def super_table_display(self):
        logger.log_info("Displaying contacts.")
        # Handle displaying contacts

        logger.log_info("Displaying contacts in a Treeview widget.")
        # Create Treeview widget
        self.super_tree = ttk.Treeview(self.super_table_frame)
        self.super_tree["columns"] = ("First Name", "Last Name", "Phone Number", "Email")

        # Define column headings
        self.super_tree.heading("#0", text="")
        self.super_tree.column("#0", anchor=tk.W, width=0)

        self.super_tree.heading("First Name", text="First Name")
        self.super_tree.column("First Name", anchor=tk.W, width=80)

        self.super_tree.heading("Last Name", text="Last Name")
        self.super_tree.column("Last Name", anchor=tk.W, width=90)

        self.super_tree.heading("Phone Number", text="Phone Number")
        self.super_tree.column("Phone Number", anchor=tk.W, width=100)

        self.super_tree.heading("Email", text="Email")
        self.super_tree.column("Email", anchor=tk.W, width=150)

        # Insert actual data from the AddressBook
        for i, contact in enumerate(address_book.contacts, 1):
            self.super_tree.insert("", "end", values=(contact.first_name, contact.last_name,
                                                      contact.phone_number, contact.email))

        # Configure scrollbar
        scrollbar = ttk.Scrollbar(self.super_table_frame, orient="vertical", command=self.super_tree.yview)
        self.super_tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        # Pack the Treeview widget
        self.super_tree.pack(expand=True, fill="both")

    def update_treeview(self):
        # Clear tree
        for item in self.super_tree.get_children():
            self.super_tree.delete(item)

        # Insert actual data from the AddressBook
        for i, contact in enumerate(address_book.contacts, 1):
            self.super_tree.insert("", "end", values=(contact.first_name, contact.last_name,
                                                      contact.phone_number, contact.email))

        # Update idletasks to refresh the Treeview
        self.super_tree.update_idletasks()

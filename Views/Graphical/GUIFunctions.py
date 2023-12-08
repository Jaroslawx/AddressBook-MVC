from utils.Log import logger
from Models.AddressBook import address_book
from Controllers.ContactController import ContactController

import tkinter as tk
from tkinter import ttk, messagebox
import sys


class GUIFunctions:
    def __init__(self, master):
        self.temp_name = None
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
        remove_button = tk.Button(remove_window, text="Remove Contact", command=remove_selected_contact)
        remove_button.pack(side=tk.LEFT, padx=5, pady=10)

        # Add a button to exit the loop and close the window
        exit_button = tk.Button(remove_window, text="Exit", command=remove_window.destroy)
        exit_button.pack(side=tk.LEFT, padx=5, pady=10)

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
        # Display a Toplevel window for sorting contacts
        sort_window = tk.Toplevel(self.root)
        sort_window.title("Sort Contacts")
        sort_window.geometry("300x200")

        # Function to handle sorting contacts
        def sort_contacts(option, reverse_flag):
            ContactController.sort_contacts(option, reverse_flag)
            messagebox.showinfo("Success",
                                f"Contacts sorted by {label_mapping[option]} in "
                                f"{'descending' if reverse_flag else 'ascending'} order.")
            GUIFunctions.display_contacts(self)

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

            asc_button = tk.Button(label_frame, text="Ascending", command=lambda l=option: sort_contacts(l, False))
            asc_button.pack(side=tk.LEFT, padx=5)

            desc_button = tk.Button(label_frame, text="Descending", command=lambda l=option: sort_contacts(l, True))
            desc_button.pack(side=tk.LEFT)

        # Add a button to exit the loop and close the window
        exit_button = tk.Button(sort_window, text="Exit", command=sort_window.destroy)
        exit_button.pack(pady=10)

        # Center the window on the screen
        GUIFunctions.center_window(sort_window)

        # Start the main loop for the Toplevel window
        sort_window.mainloop()

    def edit_contact(self):
        # Handle editing a contact
        # Display a Toplevel window to show the list of contacts
        edit_window = tk.Toplevel(self.root)
        edit_window.title("Edit Contact")
        edit_window.geometry("500x400")

        # Create a Listbox to display contacts
        contacts_listbox = tk.Listbox(edit_window, selectmode=tk.SINGLE, width=90, height=20)
        contacts_listbox.pack(padx=10, pady=10)

        # Populate the Listbox with contact names
        for contact in address_book.contacts:
            contacts_listbox.insert(tk.END, f"{contact.first_name} {contact.last_name} {contact.phone_number} "
                                            f"{contact.email}")

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
                    selected_contact.first_name = new_first_name if new_first_name else selected_contact.first_name
                    selected_contact.last_name = new_last_name if new_last_name else selected_contact.last_name
                    selected_contact.phone_number = new_phone_number if new_phone_number else selected_contact.phone_number
                    selected_contact.email = new_email if new_email else selected_contact.email

                    # Update the Listbox
                    contacts_listbox.delete(selected_index[0])
                    contacts_listbox.insert(selected_index[0], f"{selected_contact.first_name} "
                                                               f"{selected_contact.last_name} "
                                                               f"{selected_contact.phone_number} "
                                                               f"{selected_contact.email}")

                    messagebox.showinfo("Success", "Contact updated successfully.")
                    edit_contact_window.destroy()

                # Add a button to update the contact
                update_button = tk.Button(edit_contact_window, text="Update Contact", command=update_contact)
                update_button.grid(row=5, column=0, columnspan=2, pady=10)

            else:
                messagebox.showwarning("Warning", "Please select a contact to edit.")

        # Add a button to edit the selected contact
        edit_button = tk.Button(edit_window, text="Edit Selected Contact", command=edit_selected_contact)
        edit_button.pack(pady=10)

        # Add a button to exit the loop and close the window
        exit_button = tk.Button(edit_window, text="Exit", command=edit_window.destroy)
        exit_button.pack(pady=10)

        # Center the window on the screen
        GUIFunctions.center_window(edit_window)

        # Start the main loop for the Toplevel window
        edit_window.mainloop()

    @staticmethod
    def clear_contacts():
        # Handle clearing contacts
        ContactController.clear_contacts()

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
            for contact in address_book.removed_contacts:
                listbox.insert(tk.END,
                    f"{contact.first_name} {contact.last_name} {contact.phone_number} {contact.email}")

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
        # Handle exiting the program
        self.root.destroy()
        sys.exit(0)

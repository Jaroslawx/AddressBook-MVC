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

        # sort order for contacts
        self.sort_order = {"first_name": "desc", "last_name": "asc", "phone_number": "asc", "email": "asc"}

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

        # Sort contacts after adding a new one
        address_book.contacts.sort(key=lambda x: x.first_name)

        # Update the treeview
        self.update_treeview()

        # Close the window after adding the contact
        window.destroy()

    def remove_contact(self, selected_index, popup=None):
        popup.destroy()

        # Handle removing a contact
        if selected_index:
            # Confirm removal
            confirmation = messagebox.askyesno("Confirmation", "Are you sure you want to remove this contact?")
            if confirmation:
                # Remove the contact from the address book
                ContactController.remove_contact(selected_index)

                # Update the contacts treeview
                self.update_treeview()
                messagebox.showinfo("Success", "Contact removed successfully.")
            else:
                self.show_contact_popup(selected_index)
        else:
            messagebox.showwarning("Warning", "Please select a contact to remove.")

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

    def edit_contact(self, selected_index, popup=None):
        popup.destroy()

        # Get the selected contact
        selected_contact = address_book.contacts[selected_index]

        # Create a Toplevel window for editing
        edit_contact_window = tk.Toplevel(self.root)
        edit_contact_window.title("Edit Contact")
        edit_contact_window.geometry("350x150")

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

            messagebox.showinfo("Success", "Contact updated successfully.")

            # Update the treeview
            self.update_treeview()

            edit_contact_window.destroy()

            self.show_contact_popup(selected_index)

        # Add a button to update the contact
        update_button = tk.Button(edit_contact_window, text="Update Contact", command=update_contact)
        update_button.grid(row=5, column=0, columnspan=2, pady=10)

        # Add a button to cancel the update
        cancel_button = tk.Button(edit_contact_window, text="Cancel", command=edit_contact_window.destroy)
        cancel_button.grid(row=5, column=1, columnspan=2, pady=10)

        # Center the window on the screen
        GUIFunctions.center_window(edit_contact_window)

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

    def super_table_display(self, contacts=address_book.contacts):
        logger.log_info("Displaying contacts.")
        # Handle displaying contacts

        # Sort contacts before displaying them
        contacts.sort(key=lambda x: x.first_name)

        logger.log_info("Displaying contacts in a Treeview widget.")
        # Create Treeview widget
        self.super_tree = ttk.Treeview(self.super_table_frame, style="Treeview")
        self.super_tree["columns"] = ("first_name", "last_name", "phone_number", "email")

        # Add handle heading click sort
        for col in ("first_name", "last_name", "phone_number", "email"):
            self.super_tree.heading(col, text=col, command=lambda c=col: self.super_table_display_sort(c))

        # Define column headings
        self.super_tree.heading("#0", text="")
        self.super_tree.column("#0", anchor=tk.W, width=0)

        self.super_tree.heading("first_name", text="First Name")
        self.super_tree.column("first_name", anchor=tk.W, width=80)

        self.super_tree.heading("last_name", text="Last Name")
        self.super_tree.column("last_name", anchor=tk.W, width=90)

        self.super_tree.heading("phone_number", text="Phone Number")
        self.super_tree.column("phone_number", anchor=tk.W, width=100)

        self.super_tree.heading("email", text="Email")
        self.super_tree.column("email", anchor=tk.W, width=150)

        # Insert actual data from the AddressBook
        for i, contact in enumerate(contacts, 1):
            self.super_tree.insert("", "end", values=(contact.first_name, contact.last_name,
                                                      contact.phone_number, contact.email))

        # Configure scrollbar
        scrollbar = ttk.Scrollbar(self.super_table_frame, orient="vertical", command=self.super_tree.yview)
        self.super_tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        # Add style to the Treeview for lines between columns
        style = ttk.Style()
        style.configure("Treeview", background="white", fieldbackground="lightgray", borderwidth=1, relief="solid")

        # Pack the Treeview widget
        self.super_tree.pack(expand=True, fill="both")

        # Bind the click event to a function
        self.super_tree.bind("<ButtonRelease-1>", self.show_contact_details)

    def show_contact_details(self, event):
        # Get the selected item
        selected_item = self.super_tree.selection()

        if selected_item:
            # Find the index of the selected item
            index = self.super_tree.index(selected_item[0])

            # Display a popup window with contact details
            self.show_contact_popup(index)

    def show_contact_popup(self, index):
        # Create a popup window with contact details
        popup = tk.Toplevel(self.root)
        popup.title("Contact Details")

        # Set the dimensions of the popup window
        popup.geometry("275x150")

        # Get the contact based on the index
        selected_contact = address_book.contacts[index]

        # Display contact details in the popup window
        tk.Label(popup, text=f"First Name: {selected_contact.first_name}", font=("Helvetica", 10, "bold")).pack(
            anchor="w")
        tk.Label(popup, text=f"Last Name: {selected_contact.last_name}", font=("Helvetica", 10, "bold")).pack(
            anchor="w")
        tk.Label(popup, text=f"Phone Number: {selected_contact.phone_number}", font=("Helvetica", 10, "bold")).pack(
            anchor="w")
        tk.Label(popup, text=f"Email: {selected_contact.email}", font=("Helvetica", 10, "bold")).pack(anchor="w")

        # Add buttons for editing and deleting the contact
        button_frame = tk.Frame(popup)
        button_frame.pack(side=tk.BOTTOM)

        tk.Button(button_frame, text="Edit Contact", command=lambda: self.edit_contact(index, popup)).pack(
            side=tk.LEFT, padx=10, pady=10)
        tk.Button(button_frame, text="Delete Contact", command=lambda: self.remove_contact(index, popup)).pack(
            side=tk.LEFT, padx=10, pady=10)
        tk.Button(button_frame, text="Exit", command=lambda: popup.destroy()).pack(
            side=tk.LEFT, padx=10, pady=10)

        # Center the window on the screen
        GUIFunctions.center_window(popup)

        GUIFunctions.update_treeview(self)

    def super_table_display_sort(self, col):
        # Handle sorting contacts
        contacts = address_book.contacts

        # Check if the column is already sorted
        if self.sort_order[col] == "asc":
            reverse_order = False
            self.sort_order[col] = "desc"
        else:
            reverse_order = True
            self.sort_order[col] = "asc"

        # Sort contacts
        contacts.sort(key=lambda x: getattr(x, col), reverse=reverse_order)

        # Update the treeview
        self.update_treeview()

    def update_treeview(self, contacts=address_book.contacts):
        # Clear tree
        for item in self.super_tree.get_children():
            self.super_tree.delete(item)

        # Insert actual data from the AddressBook
        for i, contact in enumerate(contacts, 1):
            self.super_tree.insert("", "end", values=(contact.first_name, contact.last_name,
                                                      contact.phone_number, contact.email))

        # Update idletasks to refresh the Treeview
        self.super_tree.update_idletasks()

    def exit_program(self):
        logger.log_info("Application closed.")
        # Handle exiting the program
        self.root.destroy()
        sys.exit(0)

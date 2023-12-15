from utils.Log import logger
from Models.AddressBook import address_book
from Controllers.ContactController import ContactController

import tkinter as tk
from tkinter import ttk, messagebox
import sys


class GUIFunctions:
    def __init__(self, master, display_frame):
        self.root = master
        self.contacts_tree = None
        self.display_frame = display_frame

        # sort order for contacts
        self.sort_order = {"first_name": "desc", "last_name": "asc", "phone_number": "asc", "email": "asc"}

    def add_contact(self):
        logger.log_info("Adding a contact.")
        # Handle adding a contact
        add_window = tk.Toplevel(self.root)
        add_window.title("Add Contact")
        add_window.iconbitmap("assets/addcontact.ico")

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
        add_button = tk.Button(add_window, text="Add Contact", command=lambda: self.confirm_add_contact(
            add_window, first_name_entry.get(), last_name_entry.get(), phone_number_entry.get(), email_entry.get()))
        add_button.grid(row=5, column=0, columnspan=1, pady=10)

        # Button to cancel contact addition
        cancel_button = tk.Button(add_window, text="Cancel", command=add_window.destroy)
        cancel_button.grid(row=5, column=1, columnspan=2, pady=10)

        self.center_window(add_window)

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

        self.add_contact()

    def remove_contact(self, selected_index, popup):
        popup.destroy()

        # Handle removing a contact
        if address_book.contacts[selected_index]:
            # Confirm removal
            confirmation = messagebox.askyesno("Confirmation", "Are you sure you want to remove this contact?")
            if confirmation:
                # Remove the contact from the address book
                ContactController.remove_contact(selected_index)

                self.clear_frame(self.display_frame)
                self.contacts_display()

                messagebox.showinfo("Success", "Contact removed successfully.")
            else:
                self.show_contact_popup(selected_index)
        else:
            messagebox.showwarning("Warning", "Please select a contact to remove.")

    def edit_contact(self, selected_index, popup):
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
        def on_cancel():
            edit_contact_window.destroy()
            self.show_contact_popup(selected_index)

        # Add a button to cancel the update
        cancel_button = tk.Button(edit_contact_window, text="Cancel", command=on_cancel)
        cancel_button.grid(row=5, column=1, columnspan=2, pady=10)

        # Center the window on the screen
        GUIFunctions.center_window(edit_contact_window)

    def contacts_display(self):
        # Handle displaying contacts
        logger.log_info("Displaying contacts.")

        logger.log_info("Displaying contacts in a Treeview widget.")
        # Create Treeview widget
        self.contacts_tree = ttk.Treeview(self.display_frame, style="Treeview")
        self.contacts_tree["columns"] = ("first_name", "last_name", "phone_number", "email")

        # Add handle heading click sort
        for col in ("first_name", "last_name", "phone_number", "email"):
            self.contacts_tree.heading(col, text=col, command=lambda c=col: self.super_table_display_sort(c))

        # Define column headings
        self.contacts_tree.heading("#0", text="")
        self.contacts_tree.column("#0", anchor=tk.W, width=0)

        self.contacts_tree.heading("first_name", text="First Name")
        self.contacts_tree.column("first_name", anchor=tk.W, width=80)

        self.contacts_tree.heading("last_name", text="Last Name")
        self.contacts_tree.column("last_name", anchor=tk.W, width=90)

        self.contacts_tree.heading("phone_number", text="Phone Number")
        self.contacts_tree.column("phone_number", anchor=tk.W, width=100)

        self.contacts_tree.heading("email", text="Email")
        self.contacts_tree.column("email", anchor=tk.W, width=150)

        # Insert actual data from the AddressBook
        for i, contact in enumerate(address_book.contacts, 1):
            self.contacts_tree.insert("", "end", values=(contact.first_name, contact.last_name,
                                                         contact.phone_number, contact.email))

        # Configure scrollbar
        scrollbar = ttk.Scrollbar(self.display_frame, orient="vertical", command=self.contacts_tree.yview)
        self.contacts_tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        # Add style to the Treeview for lines between columns
        style = ttk.Style()
        style.configure("Treeview", background="white", fieldbackground="lightgray", borderwidth=1, relief="solid")

        # Pack the Treeview widget
        self.contacts_tree.pack(expand=True, fill="both")

        # Bind the click event to a function
        self.contacts_tree.bind("<ButtonRelease-1>", self.show_contact_details)

    def update_treeview(self, main_tree=True, treeview=None, contacts=address_book.contacts):
        if main_tree:
            # Clear tree
            for item in self.contacts_tree.get_children():
                self.contacts_tree.delete(item)

            # Insert actual data from the AddressBook
            for i, contact in enumerate(address_book.contacts, 1):
                self.contacts_tree.insert("", "end", values=(contact.first_name, contact.last_name,
                                                             contact.phone_number, contact.email))
            # Update idletasks to refresh the Treeview
            self.contacts_tree.update_idletasks()
        else:
            # Clear tree
            for item in treeview.get_children():
                treeview.delete(item)

            # Insert actual data from the AddressBook
            for i, contact in enumerate(contacts, 1):
                treeview.insert("", "end", values=(contact.first_name, contact.last_name,
                                                   contact.phone_number, contact.email))
            # Update idletasks to refresh the Treeview
            treeview.update_idletasks()

    def show_contact_details(self, event):
        # Get the selected item
        selected_item = self.contacts_tree.selection()

        if selected_item:
            # Find the index of the selected item
            index = self.contacts_tree.index(selected_item[0])

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

        self.update_treeview()

    def super_table_display_sort(self, col):
        # Handle sorting contacts

        # Check if the column is already sorted
        if self.sort_order[col] == "asc":
            reverse_order = False
            self.sort_order[col] = "desc"
        else:
            reverse_order = True
            self.sort_order[col] = "asc"

        # Sort contacts
        address_book.contacts.sort(key=lambda x: getattr(x, col), reverse=reverse_order)

        # Update the treeview
        self.update_treeview()

    # TODO: labels colors fix
    def show_search_popup(self, search_frame):
        input_search_frame = tk.Frame(search_frame, bg="white")
        input_search_frame.pack(side=tk.TOP, padx=5, pady=5)

        # Display the old and new values
        tk.Label(input_search_frame, text="Search Contact").pack(side=tk.TOP, anchor=tk.N)

        # Display labels and entry widgets for search criteria
        labels = ["Name:", "Surname:", "Phone Number:", "Email:"]
        entries = [tk.Entry(input_search_frame) for _ in range(len(labels))]

        for label, entry in zip(labels, entries):
            tk.Label(input_search_frame, text=label).pack(side=tk.TOP, anchor=tk.W)
            entry.pack(side=tk.TOP, anchor=tk.N)

        # Add a button to perform the search
        search_button = tk.Button(input_search_frame, text="Search", command=lambda: on_perform_search())
        search_button.pack(side=tk.LEFT, anchor=tk.N, padx=5, pady=5)

        # Add a button to perform the search
        reset_button = tk.Button(input_search_frame, text="Reset", command=lambda: self.reset_contacts())
        reset_button.pack(side=tk.LEFT, anchor=tk.N, padx=5, pady=5)

        # Add a button to perform the search
        exit_button = tk.Button(input_search_frame, text="Exit", command=lambda: on_closing())
        exit_button.pack(side=tk.LEFT, anchor=tk.N, padx=5, pady=5)

        def on_perform_search():
            address_book.contacts.extend(address_book.unmatched_contacts)
            address_book.unmatched_contacts.clear()

            self.perform_search(entries)

        def on_closing():
            self.reset_contacts()
            input_search_frame.destroy()

    def perform_search(self, entries):
        # Get search criteria from the entry widgets
        name = entries[0].get()
        surname = entries[1].get()
        phone_number = entries[2].get()
        email = entries[3].get()

        # Perform the search based on the criteria
        address_book.contacts, address_book.unmatched_contacts = ContactController.search_contact(name, surname,
                                                                                                  phone_number, email)

        # Display the search results
        self.clear_frame(self.display_frame)
        self.contacts_display()

    def reset_contacts(self):
        ContactController.reset_search()

        address_book.contacts = address_book.contacts
        address_book.unmatched_contacts = address_book.unmatched_contacts

        self.clear_frame(self.display_frame)
        self.contacts_display()

    def clear_contacts(self):
        logger.log_info("Clearing contacts.")
        # Handle clearing contacts
        ContactController.clear_contacts()

        # Update the treeview
        self.update_treeview()

    def sort_contacts(self):
        # Display a Toplevel window for sorting contacts
        sort_window = tk.Toplevel(self.root)
        sort_window.title("Sort Contacts")
        sort_window.geometry("300x200")
        sort_window.iconbitmap("assets/sort.ico")

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

    def recycle_bin(self):
        def show_removed_details(event):
            # Get the selected item
            selected_item = treeview.selection()

            if selected_item:
                # Find the index of the selected item
                index = treeview.index(selected_item[0])

                # Display a popup window with contact details
                self.removed_contact_popup(index, treeview)

        def restore_all_contacts():
            ContactController.restore_all_contacts()
            restore_window.destroy()

            self.update_treeview()
            messagebox.showinfo("Success", "All contacts restored successfully.")

        def clear_recycle_bin():
            # Clear the removed contacts
            address_book.removed_contacts.clear()

            restore_window.destroy()
            messagebox.showinfo("Success", "Recycle bin cleared successfully.")

        # Display a Toplevel window to show the list of contacts
        restore_window = tk.Toplevel(self.root)
        restore_window.title("Recycle Bin")
        restore_window.geometry("900x300")
        restore_window.iconbitmap("assets/bin.ico")

        # Create Treeview widget for the recycle bin
        treeview = ttk.Treeview(restore_window, columns=("first_name", "last_name", "phone_number", "email"),
                                show="headings", selectmode="browse")
        treeview.heading("first_name", text="First Name")
        treeview.heading("last_name", text="Last Name")
        treeview.heading("phone_number", text="Phone Number")
        treeview.heading("email", text="Email")
        treeview.pack(padx=10, pady=10)

        # Populate the Treeview with contact details from the removed contacts
        for contact in address_book.removed_contacts:
            treeview.insert("", "end", iid=contact, values=(contact.first_name, contact.last_name,
                                                            contact.phone_number, contact.email))

        # Przypisz funkcję obsługi zdarzeń do Treeview
        treeview.bind("<ButtonRelease-1>", show_removed_details)

        # Add a button to restore all contacts
        restore_all_button = tk.Button(restore_window, text="Restore All", command=restore_all_contacts)
        restore_all_button.pack(side=tk.LEFT, anchor=tk.S, padx=5, pady=10)

        # Add a button to clear the recycle bin
        clear_button = tk.Button(restore_window, text="Clear Bin", command=clear_recycle_bin)
        clear_button.pack(side=tk.LEFT, anchor=tk.S, padx=5, pady=10)

        # Add a button to exit the loop and close the window
        exit_button = tk.Button(restore_window, text="Exit", command=restore_window.destroy)
        exit_button.pack(side=tk.LEFT, anchor=tk.S, padx=5, pady=10)

        # Center the window on the screen
        GUIFunctions.center_window(restore_window)

        # Update the treeview
        self.update_treeview(False, treeview, address_book.removed_contacts)

    def removed_contact_popup(self, index, treeview):
        # Create a popup window with contact details
        popup = tk.Toplevel(self.root)
        popup.title("Removed Contact")

        # Set the dimensions of the popup window
        popup.geometry("275x150")

        # Get the contact based on the index
        selected_contact = address_book.removed_contacts[index]

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

        tk.Button(button_frame, text="Restore Contact", command=lambda: on_restore()).pack(
            side=tk.LEFT, padx=10, pady=10)
        tk.Button(button_frame, text="Delete Contact", command=lambda: on_delete()).pack(
            side=tk.LEFT, padx=10, pady=10)
        tk.Button(button_frame, text="Exit", command=lambda: on_exit()).pack(
            side=tk.LEFT, padx=10, pady=10)

        def on_restore():
            ContactController.restore_contact(index)
            self.update_treeview()
            self.update_treeview(False, treeview, address_book.removed_contacts)
            popup.destroy()

        def on_delete():
            address_book.removed_contacts.pop(index)
            self.update_treeview(False, treeview, address_book.removed_contacts)
            popup.destroy()

        def on_exit():
            popup.destroy()

        # Center the window on the screen
        GUIFunctions.center_window(popup)

    def exit_program(self):
        logger.log_info("Application closed.")
        # Handle exiting the program
        self.root.destroy()
        sys.exit(0)

    @staticmethod
    def clear_frame(frame):
        for widget in frame.winfo_children():
            widget.destroy()

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

    # TODO:
    #  - dodać w search, jak klikniesz enter to wyszukuje od razu,
    #  - poprawić odświeżanie i wyskakiwanie okna w bin
    #  - poprawić kolory w search
    #  - search można tylko raz wywołać, dodać, żeby nie było 2 na ekranie
    #  - dodać sortowanie w koszu
    #  - usunąć duplikaty w kodzie

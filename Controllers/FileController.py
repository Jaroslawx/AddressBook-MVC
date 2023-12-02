from utils.Log import logger
from Models.AddressBook import address_book
from tkinter import filedialog
from Models.Contact import Contact

import tkinter as tk
import csv
import os


class FileController:
    @staticmethod
    def load_contacts_and_add():
        root = tk.Tk()
        root.withdraw()  # Hide the main window

        # Choose the file
        file_path = filedialog.askopenfilename(
            title="Select a file with contacts",
            filetypes=[("Text files", "*.txt"), ("CSV files", "*.csv"), ("All files", "*.*")]
        )

        if file_path:
            try:
                with open(file_path, 'r') as file:
                    reader = csv.reader(file, delimiter=';')
                    contacts = []
                    for row in reader:
                        contacts.append(Contact(row[0], row[1], row[2], row[3]))

                for contact in contacts:
                    address_book.add_contact(contact)
                logger.log_info("Contacts loaded successfully!")
            except FileNotFoundError as e:
                logger.log_error(f"File '{file_path}' not found: {e}")
                raise
            finally:
                root.destroy()

    @staticmethod
    def save_contacts_to_file(filename="contact.txt", contacts=address_book.contacts):
        try:
            file_path = os.path.join("files", filename)
            with open(file_path, 'w', encoding='utf-8') as file:
                for contact in contacts:
                    file.write(f"{contact.first_name};{contact.last_name};{contact.phone_number};{contact.email}\n")
            logger.log_info("Contacts saved successfully.")
        except Exception as e:
            logger.log_error(f"Error saving contacts to file: {e}")
            raise

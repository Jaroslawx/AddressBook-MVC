import tkinter as tk


class GUI:
    def __init__(self):
        self.root = tk.Tk()

    def start_gui(self):
        # Init root window
        self.root.title("Hello World App")

        # Add Hello World
        label = tk.Label(self.root, text="Hello, World!")
        label.pack(padx=10, pady=10)

        # Starting the main program loop
        self.root.mainloop()


# create object
graphical_view = GUI()

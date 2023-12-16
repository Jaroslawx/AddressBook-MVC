class Controller:
    @staticmethod
    def choose_interface_mode():
        print("Select interface mode:")
        print("1. Textual Mode")
        print("2. Graphic Mode")
        print("3. Exit")

        while True:
            choice = input("Enter your choice (1, 2 or 3): ")
            if choice == "1":
                return "textual"
            elif choice == "2":
                return "graphic"
            elif choice == "3":
                exit()
            else:
                print("Invalid choice. Please enter 1 or 2.")

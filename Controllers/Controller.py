class Controller:
    @staticmethod
    def choose_interface_mode():
        print("Select interface mode:")
        print("1. Textual Mode")
        print("2. Graphic Mode")

        while True:
            choice = input("Enter your choice (1 or 2): ")
            if choice == "1":
                return "textual"
            elif choice == "2":
                return "graphic"
            else:
                print("Invalid choice. Please enter 1 or 2.")

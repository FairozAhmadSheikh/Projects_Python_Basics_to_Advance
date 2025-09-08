import random
def get_difficulty():
    """Gets the difficulty level from the user and returns the corresponding number range."""
    while True:
        try:
            choice = int(input("Choose a difficulty level:\n1. Easy (1-50)\n2. Medium (1-100)\n3. Hard (1-1000)\nEnter your choice (1, 2, or 3): "))
            if choice == 1:
                return 1, 50
            elif choice == 2:
                return 1, 100
            elif choice == 3:
                return 1, 1000
            else:
                print("Invalid choice. Please enter 1, 2, or 3.")
        except ValueError:
            print("Invalid input. Please enter a number.")
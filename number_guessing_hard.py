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
def play_game(min_val, max_val):
    """Handles a single round of the game and returns the number of guesses."""
    secret_number = random.randint(min_val, max_val)
    guesses = 0

    print(f"\nI've selected a new number between {min_val} and {max_val}.")
    
    while True:
        try:
            user_guess = int(input("Enter your guess: "))
            guesses += 1

            if user_guess < min_val or user_guess > max_val:
                print(f"Your guess is outside the range. Please guess a number between {min_val} and {max_val}.")
                continue
            if user_guess < secret_number:
                print("Higher!")
            elif user_guess > secret_number:
                print("Lower!")
            else:
                print(f"Congratulations! You guessed the number in {guesses} attempts.")
                return guesses
        except ValueError:
            print("Invalid input. Please enter a whole number.")
def main():
    """The main function to run the game and track scores."""
    total_games = 0
    total_guesses = 0
    
    print("Welcome to the Extended Number Guessing Game!")

    while True:
        min_val, max_val = get_difficulty()
        
        guesses = play_game(min_val, max_val)
        
        total_games += 1
        total_guesses += guesses
        print(f"\n--- Scoreboard ---")
        print(f"Games played: {total_games}")
        print(f"Average guesses per game: {total_guesses / total_games:.2f}")

        play_again = input("\nDo you want to play another game? (yes/no): ").lower()
        if play_again != 'yes':
            print("Thanks for playing! Goodbye.")
            break
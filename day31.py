import random
import time
from functools import lru_cache
from concurrent.futures import ThreadPoolExecutor, as_completed

# 1. Fibonacci Sequence with Memoization
@lru_cache(maxsize=128)
def fibonacci(n):
    """
    Calculates the nth Fibonacci number using memoization (caching).
    This makes it very efficient for larger numbers.
    """
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)
# 2. Parallel Processing with ThreadPoolExecutor
def calculate_fibonacci_parallel(numbers):
    """
    Calculates Fibonacci numbers for a list of numbers in parallel
    using a ThreadPoolExecutor.  This speeds up the calculation
    when you have multiple numbers to process.
    """
    results = {}
    with ThreadPoolExecutor(max_workers=4) as executor:  # Use a maximum of 4 threads
        future_to_number = {executor.submit(fibonacci, n): n for n in numbers}
        for future in as_completed(future_to_number):
            n = future_to_number[future]
            try:
                result = future.result()
                results[n] = result
            except Exception as exc:
                print(f'Fibonacci({n}) generated an exception: {exc}')
                results[n] = None  # Store None to indicate an error
    return results
# 3. Interactive Component: Number Guessing Game
def number_guessing_game():
    """
    A fun, interactive number guessing game.
    """
    secret_number = random.randint(1, 100)
    attempts = 0

    print("\nWelcome to the Number Guessing Game!")
    print("I'm thinking of a number between 1 and 100.")

    while True:
        try:
            guess = int(input("Enter your guess: "))
            attempts += 1
        except ValueError:
            print("Invalid input. Please enter a number.")
            continue

        if guess < secret_number:
            print("Too low!")
        elif guess > secret_number:
            print("Too high!")
        else:
            print(f"Congratulations! You guessed the number in {attempts} attempts.")
            break
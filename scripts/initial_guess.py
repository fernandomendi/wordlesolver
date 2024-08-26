"""
This script simulates all possible answers for an initial word in the Wordle game and stores the results in a dictionary for future reference. The simulation calculates which words remain possible after each possible feedback pattern based on the initial guess, and it saves this data for quick lookups later.

Functions:
- simulation(language: str) -> None: Simulates all possible feedback patterns for the initial guess and stores the resulting data in a cache.

Main Functionality:
- The script accepts a language code as a command-line argument.
- It retrieves the best initial guess for the specified language.
- It generates all possible feedback patterns (combinations of correct, misplaced, and absent letters).
- For each pattern, it filters the possible words and calculates their entropies.
- The results are stored in a dictionary and written to a JSON file for future use.
"""

from itertools import product
import sys

from wordlesolver.common import theory
from wordlesolver.common.variables import Language, Status


def simulation(language: str) -> None:
    """
    Simulate all possible answers based on an initial word for a given language.

    Args:
    - language (str): The language code to use (e.g., 'ES' for Spanish).

    Returns:
    - None: The function saves the results to a JSON file instead of returning them.
    
    Process:
    - Retrieves the best initial guess based on the specified language.
    - Generates all possible combinations of feedback patterns (correct, misplaced, absent).
    - Filters the possible words and calculates the entropy for each pattern.
    - Stores the results in a dictionary for quick reference in future games.
    """

    # Retrieve the best initial guess for the specified language.
    initial_guess: str = Language().best_initial_guess(language)

    # Generate all possible combinations of feedback patterns.
    possible_answers = product(
        [Status.CORRECT, Status.MISPLACED, Status.ABSENT],
        repeat=5
    )
    for answer in possible_answers:
        answer_str = "".join(answer)
        print(f"Calculating entropies for {answer_str}")

        # Calculate entropies for these steps and cache them in memory.
        theory.calculate_entropies([{
            "guess" : initial_guess,
            "answer" : answer_str
        }], language)

# This ensures that the `simulate()` function is called only when the script is executed directly, and not when it is imported as a module in another script.
if __name__ == "__main__":
    if len(sys.argv) == 1:
        raise ValueError("Missing language parameter")

    input_language = getattr(Language, sys.argv[1])

    simulation(input_language)

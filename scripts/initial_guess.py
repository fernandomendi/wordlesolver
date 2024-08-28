"""
This script simulates all possible answers for an initial guess in the Wordle game and stores the results in a dictionary for future reference. The simulation calculates the entropies for the words remaining after filtering by each possible feedback pattern based on the initial guess, and it saves this data for quick lookups later.

Functions:
- simulation(language: str) -> None: Simulates all possible feedback patterns for the initial guess and stores the resulting data in a cache.

Main Functionality:
- The script accepts a language code as a command-line argument.
- It retrieves the best initial guess for the specified language.
- It generates all possible feedback patterns (combinations of correct, misplaced, and absent letters).
- For each pattern, it calculates the entropies for the corresponding guess-answer combination.
- The results are cached for future use.
"""

from itertools import product
import sys

from wordlesolver.common import theory
from wordlesolver.common.core.variables import Language, Languages, Status


def simulation(language_code: str) -> None:
    """
    Simulate all possible answers based on an initial word for a given language.

    Parameters:
    -----------
    language_code : str
        Language code to choose reference file to query and initial best guess.

    Returns:
    --------
    None
        The function caches the possible entropies for future use.
    """

    language: Language = Languages().from_code(language_code)

    # Retrieve the best initial guess for the specified language.
    initial_guess: str = language.best_initial_guess

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

    # Unpack values from command line input
    in_language, = sys.argv[1:]

    simulation(in_language)

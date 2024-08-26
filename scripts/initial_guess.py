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
import json
import sys

from wordlesolver.common import query, theory
from wordlesolver.common.variables import Language, Status

import pandas as pd


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

    # Retrieve the best initial guess for the specified language
    initial_guess: str = Language().best_initial_guess(language)
    cache: dict = {
        initial_guess: {}
    }

    # Generate all possible combinations of feedback patterns
    possible_answers = product(
        [Status.CORRECT, Status.MISPLACED, Status.ABSENT],
        repeat=5
    )
    for answer in possible_answers:

        # Filter the words based on the current feedback pattern
        possible_words: pd.DataFrame = query.filter_words_accumulative(
            steps=[{
                "guess" : initial_guess, 
                "answer" : answer
            }],
            language=language
        )

        # Calculate entropies for the remaining possible words
        stats_words: pd.DataFrame = theory.calculate_entropies(possible_words, language)

        cache[initial_guess]["".join(answer)] = list(
            stats_words \
                .to_dict(orient="index") \
                .values()
        )

    with open("data/es/cache/initial_guess.json", "w") as f:
        json.dump(cache, f, indent=4)


# This ensures that the `simulate()` function is called only when the script is executed directly, and not when it is imported as a module in another script.
if __name__ == "__main__":
    if len(sys.argv) == 1:
        raise ValueError("Missing language parameter")

    input_language = getattr(Language, sys.argv[1])
    simulation(Language.ES)

from math import exp
import os
import shutil
import sys

from wordlesolver.common.core.variables import Language, Languages

import pandas as pd
import numpy as np

from wordlesolver.common.validation import validate_word


def sigmoid(x: float) -> float:
    """
    Applies the sigmoid function to a given input x.

    Parameters:
    -----------
    x : float
        The input value.

    Returns:
    --------
    float
        The sigmoid of x, a value between 0 and 1.
    """
    return 1/(1 + exp(-x))


def simulation(word: str, language: Language) -> None:
    """
    Simulates the removal of a word from a list of words, updating probabilities for the remaining words.

    This function reads a CSV file containing a list of words, checks if the given word exists, removes it if found, and recalculates the probabilities of the remaining words using a sigmoid function. The updated list is saved back to the CSV file. Additionally, it clears the cache by deleting any pre-existing cache directory.

    Parameters:
    -----------
    word : str
        The word to be removed from the list.
    language_code : str
        Language code to choose reference file to query and initial best guess.
    """

    # Define the path to the words file based on the language
    words_path = f"data/{language.code}/words.csv"
    words = pd.read_csv(words_path)[["word"]]

    # Check if the word exists in the list
    is_word = any(words.word == word)

    if not is_word:
        print(f"Word '{word}' is not in words file.")

    else:
        # Filter out the specified word and reset indices
        filtered_words = words[words.word != word] \
            .reset_index() \
            .reset_index() \
            .rename(columns={
                "level_0" : "id"
            })[["id", "word"]]

        filtered_words["id"] += 1

        total_words = len(filtered_words)

        # Generate an array of values between -10 and 10 for sigmoid calculation
        x_vals = np.linspace(-10, 10, total_words)

        # Apply the sigmoid function to calculate probabilities for each remaining word
        filtered_words["probability"] = filtered_words.id \
            .apply(lambda x: sigmoid(x_vals[total_words - (x)]))

        filtered_words.to_csv(words_path, index=False)

        # Define the path to the cache directory and remove it if it exists
        cache_path = f"data/{language.code}/cache"
        if os.path.exists(cache_path):
            shutil.rmtree(cache_path)

        print(f"Removed word: '{word}' from words file.")


# This ensures that the `simulate()` function is called only when the script is executed directly, and not when it is imported as a module in another script.
if __name__ == "__main__":

    # Unpack values from command line input
    in_word, in_language, = sys.argv[1:]

    # Reformat parameters
    in_language: Language = Languages().from_code(in_language)

    # Validate input
    validate_word(in_word, in_language)

    simulation(in_word, in_language)

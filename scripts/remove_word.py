from math import exp
import os
import shutil
import sys

from wordlesolver.common.variables import Language

import pandas as pd
import numpy as np


def sigmoid(x):
    return 1/(1 + exp(-x))


def simulation(word: str, language: str) -> None:
    words_path = f"data/{language}/words.csv"
    words = pd.read_csv(words_path)[["word"]]

    is_word = any(words.word == word)

    if not is_word:
        print(f"Word '{word}' is not in words file.")

    else:
        filtered_words = words[words.word != word] \
            .reset_index() \
            .reset_index() \
            .rename(columns={
                "level_0" : "id"
            })[["id", "word"]]

        filtered_words["id"] += 1

        total_words = len(filtered_words)

        x_vals = np.linspace(-10, 10, total_words)

        filtered_words["probability"] = filtered_words.id \
            .apply(lambda x: sigmoid(x_vals[total_words - (x)]))

        filtered_words.to_csv(words_path, index=False)

        cache_path = f"data/{language}/cache"
        if os.path.exists(cache_path):
            shutil.rmtree(cache_path)

        print(f"Removed word: '{word}' from words file.")


# This ensures that the `simulate()` function is called only when the script is executed directly, and not when it is imported as a module in another script.
if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise ValueError("Wrong number of inputs")

    input_word = sys.argv[1]
    input_language = getattr(Language, sys.argv[2])

    simulation(input_word, input_language)

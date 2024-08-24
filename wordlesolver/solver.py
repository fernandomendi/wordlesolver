import pandas as pd
from tqdm import tqdm
tqdm.pandas()

from common import theory
from common.variables import reformat_answer

def wordle() -> None:
    """
    A function to simulate and guide you through a command-line Wordle game using a predefined list of words and calculated probabilities.

    The game involves:
    1. Loading a list of possible words and their associated probabilities.
    2. Iteratively narrowing down the list of possible words based on user guesses and feedback.
    3. Recommending the best next guess based on entropy calculation until only one word remains.
    """
    # Load the list of words and their probabilities from the CSV file
    words = pd.read_csv("data/probabilities_es.csv")
    all_words = words
    possible_words = words

    # Start with a predefined guess -> this has been proven to be the most effective first guess
    guess = "careo"

    # Loop until only one possible word remains
    while len(possible_words) > 1:
        print(f"Best guess: {guess}")

        guess = input("Guess: ")
        answer = input("Answer: ")

        # Reformat answer (str) as a list of statuses objects
        answer_status = reformat_answer(answer)

        possible_words = theory.filter_words(possible_words, guess, answer_status)

        # Preview the top few remaining words
        print(f"There are {len(possible_words)} possible words")
        print(possible_words.head())

        # If more than one word remains, calculate entropies and determine the best next guess
        if len(possible_words) != 1:
            stats_words = theory.calculate_entropies(all_words, possible_words)
            guess = theory.best_guess(stats_words, 1)

    # When only one possible word remains, it is the secret word
    secret = possible_words.reset_index().loc[0].word
    print(f"The only word left is: {secret}")

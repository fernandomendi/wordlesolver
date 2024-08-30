import sys

from wordlesolver.common import feedback
from wordlesolver.core.variables import Language, Languages
from wordlesolver.filter import filter_words_accumulative
from wordlesolver.theory import best_guess

import pandas as pd
from tqdm import tqdm
tqdm.pandas()


def steps_per_secret(secret: str, language: Language) -> int:
    """
    Simulates the process of guessing a secret word in the given language, returning the sequence of steps taken.

    Parameters
    ----------
    secret : str
        The secret word that needs to be guessed.
    language : Language
        The language object containing the word list and other relevant data.

    Returns
    -------
    int
        The number of steps taken to find the solution using the suggested guesses.
    """

    steps = []
    possible_words = filter_words_accumulative(steps, language)

    # Continue the loop while there is more than one possible word and fewer than 6 steps have been taken.
    while len(possible_words) > 1 and len(steps) < 6:
        guess = best_guess(steps, language)
        answer = feedback(secret, guess)
        steps.append({
            "guess" : guess,
            "answer" : answer
        })

        possible_words = filter_words_accumulative(steps, language)

    # If there is only one possible word left, make the final guess.
    guess = possible_words.loc[0, "word"]
    answer = feedback(secret, guess)
    steps.append({
        "guess" : guess,
        "answer" : answer
    })

    # Return the total number of steps taken to guess the secret word.
    return len(steps)


def simulation(language: Language, sample_size: int) -> None:
    """
    Simulates the word-guessing process across a sample of words in the given language, and prints the results.

    Parameters
    ----------
    language : Language
        The language object containing the word list and other relevant data.
    entropy_weight : float
        A weighting factor used in the entropy-based guessing strategy.
    filter_weight : float
        A weighting factor used in the entropy-based guessing strategy.
    sample_size : int
        The number of words to sample from the word list for the simulation.

    Returns
    -------
    None
    """

    words = pd.read_csv(f"data/{language.code}/words.csv") \
        .sample(n=sample_size)

    words["steps"] = words.word.progress_apply(lambda x: steps_per_secret(x, language))

    steps_aggregated = words.steps.value_counts().reset_index()
    steps_aggregated.steps = steps_aggregated.steps.replace(7, "6+")
    steps_aggregated["probability"] = steps_aggregated["count"] / len(words)
    steps_aggregated = steps_aggregated[["steps", "probability"]]

    print("Average steps per word")
    output = steps_aggregated.to_string(formatters={
        'probability': '{:,.2%}'.format
    })
    print(output)


# This ensures that the `simulate()` function is called only when the script is executed directly, and not when it is imported as a module in another script.
if __name__ == "__main__":

    # Unpack values from command line input
    in_language, in_entropy_weight, in_filter_weight, in_sample_size = sys.argv[1:]

    # Reformat parameters
    in_language: Language = Languages().from_code(in_language)
    in_sample_size: int = int(in_sample_size)

    simulation(in_language, in_sample_size)

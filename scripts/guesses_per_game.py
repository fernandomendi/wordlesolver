import sys

from wordlesolver.common.core.variables import Language, Languages
from wordlesolver.common.query import filter_words_accumulative
from wordlesolver.common.theory import best_guess, feedback, get_entropies

import pandas as pd
from tqdm import tqdm

from wordlesolver.common.validation import validate_weight
tqdm.pandas()


def steps_per_secret(secret: str, language: Language) -> list[dict[str, str]]:

    steps = []
    possible_words = filter_words_accumulative(steps, language)

    while len(possible_words) > 1:
        stats = get_entropies(steps, language)

        guess = best_guess(stats, 0.5)
        answer = feedback(secret, guess)
        steps.append({
            "guess" : guess,
            "answer" : answer
        })

        possible_words = filter_words_accumulative(steps, language)

    guess = possible_words.loc[0, "word"]
    answer = feedback(secret, guess)
    steps.append({
        "guess" : guess,
        "answer" : answer
    })

    return len(steps)


def simulation(language: Language) -> None:
    words = pd.read_csv(f"data/{language.code}/words.csv")

    words["steps"] = words.word.progress_apply(lambda x: steps_per_secret(x, language))

    steps_aggregated = words.steps.value_counts().reset_index()
    steps_aggregated["count"] /= len(words)

    print(steps_aggregated)


# This ensures that the `simulate()` function is called only when the script is executed directly, and not when it is imported as a module in another script.
if __name__ == "__main__":

    # Unpack values from command line input
    in_language, in_weight = sys.argv[1:]

    # Reformat parameters
    in_language: Language = Languages().from_code(in_language)

    # Validate input
    validate_weight(in_weight)

    simulation(in_language)

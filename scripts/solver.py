import sys

from wordlesolver.core.common import validate_answer, validate_word
from wordlesolver.core.exceptions import InvalidAnswerError, InvalidWordLengthError, WordNotFoundError
from wordlesolver.core.variables import Language, Languages
from wordlesolver.filter import filter_words_accumulative
from wordlesolver.theory import get_entropies, best_guess

import pandas as pd


def wordle(language_code: str) -> None:
    """
    Runs an interactive Wordle-solving loop where the user inputs guesses and feedback, and the program narrows down the possible secret words until it finds the correct one. The program uses entropy-based guessing to improve its chances of identifying the secret word efficiently.

    The function uses a list of steps (each containing a guess and the corresponding feedback) to filter the list of possible words iteratively. It continues suggesting the best possible guess based on the remaining words, until the secret word is identified.
    
    Parameters:
    -----------
    language_code : str
        Language code to choose reference file to query and initial best guess.

    Workflow:
    ---------
    1. **Initialization**:
        - Set `best_guess` to a default starting word depending on the language.
        - Initialize an empty list `steps` to store the guess-feedback pairs.
        - Initialize `secret_found` as `False` to control the loop until the secret word is identified.

    2. **Main Loop**:
        - The loop continues until the secret word is found (`secret_found` becomes `True`).
        - Display the current best guess to the user.
        - Prompt the user to input their guess and the corresponding feedback (`answer`).
        - Store the guess and feedback as a step in the `steps` list.

    3. **Filtering Words**:
        - Use the `filter_words_accumulative` function to filter the list of possible words based on all accumulated steps.
        - Display the number of remaining possible words and preview the top few.

    4. **Check for Secret Word**:
        - If only one possible word remains, it is identified as the secret word, and the loop ends.
        - If multiple words remain, the program calculates the entropy of each word and determines the next best guess using `best_guess`.

    5. **Finding the Secret Word**:
        - Once the loop ends (when only one word remains), the secret word is displayed to the user.
    """

    language: Language = Languages().from_code(language_code)

    # Initial setup: starting guess, empty list of steps, and secret found flag
    initial_guess: str = language.initial_suggestion
    suggested_guess: str = initial_guess
    steps: list[dict[str, str]] = []
    secret_found: bool = False

    # Main loop: continue until the secret word is found
    while not secret_found:
        print(f"Suggested guess: {suggested_guess}")

        # Prompt user for a valid guess
        valid_guess = False
        while not valid_guess:
            guess: str = input("Guess: ")
            try:
                valid_guess = validate_word(guess, language)
            except (InvalidWordLengthError, WordNotFoundError) as e:
                print(e)

        # Prompt user for a valid answer
        valid_answer = False
        while not valid_answer:
            answer: str = input("Answer: ")
            try:
                valid_answer = validate_answer(answer)
            except InvalidAnswerError as e:
                print(e)

        steps.append({
            "guess" : guess,
            "answer" : answer,
        })

        # Filter the list of possible words based on all steps so far
        possible_words: pd.DataFrame = filter_words_accumulative(steps, language)

        # Preview the top few remaining words
        print(f"There are {len(possible_words)} possible words")
        print(possible_words.head())

        # When only one possible word remains, it is the secret word
        if len(possible_words) == 1:
            secret_found: bool = True
            secret: str = possible_words.reset_index().loc[0].word
            print(f"The only word left is: {secret}")

        # If multiple words remain, calculate entropies and determine the best next guess
        else:
            stats_words = get_entropies(steps, language)
            suggested_guess = best_guess(stats_words, 1)


# This ensures that the `wordle()` function is called only when the script is executed directly, and not when it is imported as a module in another script.
if __name__ == "__main__":

    # Unpack values from command line input
    in_language, = sys.argv[1:]

    wordle(in_language)

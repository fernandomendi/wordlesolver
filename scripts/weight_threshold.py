from itertools import product
import sys

from wordlesolver.core.variables import Language, Languages, Status
from wordlesolver.filter import filter_words_accumulative


def simulation(language: Language):
    """
    Simulates the filtering process for a given language to determine the maximum number of possible words remaining after applying the initial suggestion and all possible feedback combinations.

    Parameters:
    -----------
    language : Language
        A Language object that contains information such as the language code and the best initial suggestion.
    
    Returns:
    --------
    None
        The function prints the maximum number of words remaining after filtering with the initial word.
    """

    threshold = 0

    # Generate all possible combinations of feedback statuses for a 5-letter word
    possible_answers = product(
        [Status.CORRECT, Status.MISPLACED, Status.ABSENT],
        repeat=5
    )

    # Iterate over each possible answer (feedback combination)
    for answer in possible_answers:
        answer_str = "".join(answer)

        # Filter the list of possible words based on the initial guess and this feedback combination
        possible_words = filter_words_accumulative([{
            "guess": language.initial_suggestion,
            "answer": answer_str
        }], language)

        # Update the threshold to the maximum number of words remaining after any filtering
        threshold = max(len(possible_words), threshold)

    print(f"The maximum number of words after filtering with initial word '{language.initial_suggestion}' is {threshold}")


# This ensures that the `simulate()` function is called only when the script is executed directly, and not when it is imported as a module in another script.
if __name__ == "__main__":

    # Unpack values from command line input
    in_language, = sys.argv[1:]

    # Reformat parameters
    in_language: Language = Languages().from_code(in_language)

    simulation(in_language)

from wordlesolver.common import theory
from wordlesolver.common.variables import Status

import pandas as pd


def filter_words(words: pd.DataFrame, guess: str, answer: list[str]) -> pd.DataFrame:
    """
    Filters the words dataframe to find words that match the given guess and expected feedback.

    Parameters:
    ----------
    words : pd.DataFrame
        DataFrame containing a column 'word' with possible words.
    guess : str
        The guessed word to be used for comparison. It should be a 5-letter string.
    answer : list[Status]
        List of Status objects representing the expected feedback for the guess.

    Returns:
    -------
    pd.DataFrame
        A DataFrame containing only the words that match the given feedback.
    """

    # Apply the feedback function and filter based on the expected answer
    filtered_words = words[
        words.word.apply(
            lambda secret: theory.feedback(secret, guess) == answer
        )
    ]

    return filtered_words.reset_index(drop=True)


def filter_words_accumulative(steps: list[dict[str, str]], language: str) -> pd.DataFrame:
    """
    Filters a list of possible Wordle words based on multiple guess-answer pairs, applied cumulatively.

    Parameters:
    -----------
    steps : list[dict[str, str]]
        A list of dictionaries, where each dictionary contains:
        - "guess"  : str : A word that was guessed.
        - "answer" : str : The feedback received for the guess, represented as a string of digits (e.g., "22220" where '2' means absent, '1' means misplaced, and '0' means correct).
    language : str
        Language to choose reference file to query.

    Returns:
    --------
    pd.DataFrame
        A DataFrame containing the list of words that remain possible after applying all the guess-answer pairs in the provided steps list.

    Workflow:
    ---------
    1. **Base Case**: If there is only one step in the list:
        - Load the full list of words from "data/es/words.csv".
        - Apply the `filter_words` function to narrow down the possible words based on the first guess-answer pair.
    
    2. **Recursive Case**: If there are multiple steps:
        - Recursively call `filter_words_accumulative` on all but the last step to get the filtered word list up to that point.
        - Apply the `filter_words` function again using the guess-answer pair from the last step to further narrow down the list.
    
    3. **Return**: The final list of possible words after all filters have been applied.

    Notes:
    ------
    - The function is recursive, which allows it to handle any number of steps.
    - The filtering process is cumulative, meaning each step's filtering is based on the results of all previous steps.
    """

    # Base case: if there is only one step, load the words and apply the first filter
    if len(steps) == 1:
        step = steps[0]

        # Load the full list of words from the CSV file
        words = pd.read_csv(f"data/{language}/words.csv")[["word", "probability"]]

        # Apply the filter based on the first guess and its corresponding answer
        possible_words = filter_words(
            words,
            step["guess"],
            Status().reformat_answer(step["answer"])
        )

    # Recursive case: process all steps except the last one first
    else:
        step = steps[-1]

        # Recursively filter words using all previous steps
        possible_words = filter_words_accumulative(steps[:-1], language)

        # Apply the filter based on the last guess and its corresponding answer
        possible_words = filter_words(
            possible_words,
            step["guess"],
            Status().reformat_answer(step["answer"])
        )

    return possible_words

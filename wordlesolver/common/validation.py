import re

import pandas as pd


def validate_word(word: str, language: str) -> bool:
    """
    Validates whether a given word exists in the word list for a specified language.

    Parameters
    ----------
    word : str
        The word to validate.
    language : str
        The language code used to select the appropriate word list.

    Returns
    -------
    bool
        True if the word exists in the word list, False otherwise.
    """

    words: pd.DataFrame = pd.read_csv(f"data/{language}/words.csv")
    is_word: bool = any(words.word == word)

    return is_word


def validate_answer(answer: str) -> bool:
    """
    Validates whether a given answer string is a valid Wordle-style answer.
    A valid answer consists of exactly 5 characters, each being either '0', '1', or '2'.

    Parameters
    ----------
    answer : str
        The answer string to validate.

    Returns
    -------
    bool
        True if the answer is valid, False otherwise.
    """
    
    pattern: re.Pattern = re.compile("^[012]{5}$")
    is_answer: bool = pattern.match(answer)

    return is_answer

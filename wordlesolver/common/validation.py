import re

import pandas as pd


def validate_word(word: str, language: str) -> bool:
    """
    Validates whether a given word exists in the word list for a specified language. Raises an exception if the word does not exist.

    Parameters
    ----------
    word : str
        The word to validate.
    language : str
        The language code used to select the appropriate word list.

    Returns
    -------
    bool
        True if the word exists in the word list.

    Raises
    ------
    ValueError
        If the word does not exist in the word list.
    """

    words: pd.DataFrame = pd.read_csv(f"data/{language}/words.csv")

    is_word: bool = any(words.word == word)

    if not is_word:
        raise ValueError(f"The word '{word}' does not exist in the {language} word list.")

    return is_word


def validate_answer(answer: str) -> bool:
    """
    Validates whether a given answer string is a valid Wordle-style answer. A valid answer consists of exactly 5 characters, each being either '0', '1', or '2'. Raises an exception if the answer is invalid.

    Parameters
    ----------
    answer : str
        The answer string to validate.

    Returns
    -------
    bool
        True if the answer is valid.

    Raises
    ------
    ValueError
        If the answer string is not valid.
    """

    pattern: re.Pattern = re.compile("^[012]{5}$")

    is_answer: bool = pattern.match(answer)

    if not is_answer:
        raise ValueError(f"The answer '{answer}' is not a valid Wordle-style answer. It must be exactly 5 characters long, with each character being '0', '1', or '2'.")

    return is_answer

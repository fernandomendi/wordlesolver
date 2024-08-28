import re

from wordlesolver.common.core import exceptions
from wordlesolver.common.core.variables import Language

import pandas as pd


def validate_word(word: str, language: str) -> bool:
    """
    Validates whether a given word exists in the word list for a specified language. Additionally checks if the word is exactly 5 letters long. Raises exceptions if the word is invalid.

    Parameters
    ----------
    word : str
        The word to validate.
    language : str
        The language code used to select the appropriate word list.

    Returns
    -------
    bool
        True if the word is valid and exists in the word list.

    Raises
    ------
    InvalidWordLengthError
        If the word is not exactly 5 letters long.
    WordNotFoundError
        If the word does not exist in the word list.
    """

    if len(word) != 5:
        raise exceptions.InvalidWordLengthError(word)

    words: pd.DataFrame = pd.read_csv(f"data/{language}/words.csv")
    is_word: bool = any(words.word == word)

    if not is_word:
        raise exceptions.WordNotFoundError(word, language)

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
    InvalidAnswerError
        If the answer string is not valid.
    """

    # Compile a regular expression pattern that matches exactly 5 characters, each '0', '1', or '2'.
    pattern: re.Pattern = re.compile("^[012]{5}$")
    is_answer: bool = pattern.match(answer)

    if not is_answer:
        raise exceptions.InvalidAnswerError(answer)

    return is_answer


def validate_language(language: str) -> bool:
    """
    Validates if the given language is an attribute of the Language class.
    
    Parameters
    ----------
    language : str
        The language to validate.
    
    Returns
    -------
    bool
        True if the language is valid, raises InvalidLanguageError otherwise.
    
    Raises
    ------
    InvalidLanguageError
        If the language is not an attribute of the Language class.
    """
    if not hasattr(Language, language):
        raise exceptions.InvalidLanguageError(language)

    return True

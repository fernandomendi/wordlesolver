import re

from wordlesolver.core.exceptions import InvalidAnswerError, InvalidWeightError, InvalidWordLengthError, WordNotFoundError
from wordlesolver.core.variables import Language

import pandas as pd



def validate_word(word: str, language: Language) -> bool:
    """
    Validates whether a given word exists in the word list for a specified language. Additionally checks if the word is exactly 5 letters long. Raises exceptions if the word is invalid.

    Parameters
    ----------
    word : str
        The word to validate.
    language : Language
        The language used to select the appropriate word list.

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
        raise InvalidWordLengthError(word)

    words: pd.DataFrame = pd.read_csv(f"data/{language.code}/words.csv")
    is_word: bool = any(words.word == word)

    if not is_word:
        raise WordNotFoundError(word, language)

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
    is_answer: bool = bool(pattern.match(answer))

    if not is_answer:
        raise InvalidAnswerError(answer)

    return is_answer


def validate_steps(steps: list[dict[str, str]], language: Language) -> bool:
    """
    Validates whether a set of steps is valid by checking each step.

    Parameters
    ----------
    steps : list[dict[str, str]]
        A list of dictionaries where each dictionary represents a guess and its corresponding outcome (answer). Each dictionary in the list should have the following structure:
        {
            "guess": "word_guessed",
            "answer": "feedback_code"
        }
        The "guess" is the word guessed, and "answer" is the feedback received (a string representing the status of each letter).

    language : Language
        A Language object for which the word list and cache files are to be loaded. This language's code is used to access the correct files within the `data/{language.code}/` directory.

    Returns
    -------
    bool
        True if the steps are valid.

    Raises
    ------
    InvalidWordLengthError
        If the word is not exactly 5 letters long.
    WordNotFoundError
        If the word does not exist in the word list.
    InvalidAnswerError
        If the answer string is not valid.
    """

    is_valid: bool = True

    for step in steps:
        guess = step["guess"]
        answer = step["answer"]

        # Validate step
        is_valid &= validate_word(guess, language)
        is_valid &= validate_answer(answer)

    return is_valid


def validate_weight(weight: float) -> bool:
    """
    Validates whether a given value is a valid guess weight. A valid guess weight a value between 0 and 1. Raises an exception if the weight is invalid.

    Parameters
    ----------
    weight : str
        The weight value to validate.

    Returns
    -------
    bool
        True if the weight is valid.

    Raises
    ------
    InvalidWeightError
        If the weight value is not valid.
    """

    is_valid: bool = 0 <= weight <= 1

    if not is_valid:
        raise InvalidWeightError(weight)

    return is_valid

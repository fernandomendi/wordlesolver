import re
from importlib import resources

from core.exceptions import InvalidAnswerError, InvalidWordLengthError, WordNotFoundError
from core.language import Language, Step

import pandas as pd


def _load_words(language: Language) -> pd.DataFrame:
    with resources.files("core.data").joinpath(f"{language.code}/words.csv").open("r") as f:
        return pd.read_csv(f)


def validate_word(word: str, language: Language) -> bool:
    if len(word) != 5:
        raise InvalidWordLengthError(word)

    words = _load_words(language)
    is_word: bool = any(words.word == word)

    if not is_word:
        raise WordNotFoundError(word, language)

    return is_word


def validate_answer(answer: str) -> bool:
    pattern: re.Pattern = re.compile("^[012]{5}$")
    is_answer: bool = bool(pattern.match(answer))

    if not is_answer:
        raise InvalidAnswerError(answer)

    return is_answer


def validate_steps(steps: list[Step], language: Language) -> bool:
    is_valid: bool = True

    for step in steps:
        is_valid &= validate_word(step.guess, language)
        is_valid &= validate_answer(step.answer)

    return is_valid

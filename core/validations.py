import re

from core.filter import _load_words
from core.models import Language


def validate_word(word: str, language: Language) -> None:
    if len(word) != 5:
        raise ValueError(f"'{word}' must be exactly 5 characters long.")
    if not any(_load_words(language).word == word):
        raise ValueError(f"'{word}' not found in the {language.code} word list.")


def validate_answer(answer: str) -> None:
    if not re.fullmatch(r"[012]{5}", answer):
        raise ValueError(f"'{answer}' is not valid feedback. Must be 5 characters of 0, 1, or 2.")

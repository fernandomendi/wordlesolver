import re

from core.exceptions import InvalidAnswerError, InvalidWordLengthError, WordNotFoundError
from core.filter import _load_words
from core.models import Language


def validate_word(word: str, language: Language) -> bool:
    if len(word) != 5:
        raise InvalidWordLengthError(word)

    words = _load_words(language)
    if not any(words.word == word):
        raise WordNotFoundError(word, language)

    return True


def validate_answer(answer: str) -> bool:
    if not re.fullmatch(r"[012]{5}", answer):
        raise InvalidAnswerError(answer)

    return True

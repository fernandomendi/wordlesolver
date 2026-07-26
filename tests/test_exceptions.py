from core.validations import validate_word
from core.models import Language, Languages

import pytest


@pytest.mark.parametrize(
    "word, language",
    [
        ("code", Languages.EN),
        ("python", Languages.EN),
        ("area", Languages.ES),
        ("wordle", Languages.ES),
    ]
)
def test_invalid_word_length(word: str, language: Language):
    with pytest.raises(ValueError):
        validate_word(word, language)


@pytest.mark.parametrize(
    "word, language",
    [
        ("aaaaa", Languages.ES),
        ("aaaaa", Languages.EN),
        ("phone", Languages.ES),
        ("coche", Languages.EN),
    ]
)
def test_word_not_found(word: str, language: Language):
    with pytest.raises(ValueError):
        validate_word(word, language)


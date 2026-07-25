from core.validations import validate_answer, validate_word
from core.exceptions import InvalidAnswerError, InvalidWordLengthError, WordNotFoundError
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
    with pytest.raises(InvalidWordLengthError):
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
    with pytest.raises(WordNotFoundError):
        validate_word(word, language)


@pytest.mark.parametrize(
    "answer",
    [
        "000000",
        "00003",
        "coche",
    ]
)
def test_invalid_answer(answer: str):
    with pytest.raises(InvalidAnswerError):
        validate_answer(answer)


@pytest.mark.parametrize(
    "steps, language",
    [
        ([                                  # Example game in Spanish
            ("careo", "12110"),
            ("recto", "11120"),
        ], Languages.ES),
        ([                                  # Example game in English
            ("tares", "12221"),
            ("moust", "12211"),
        ], Languages.EN),
    ]
)
def test_valid_steps(steps: list[tuple], language: Language):
    solver = __import__("core").Solver(language)
    for guess, answer in steps:
        solver.add_step(guess, answer)
    assert solver.total_possible() >= 0

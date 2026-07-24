from core.validations import validate_answer, validate_steps, validate_word
from core.exceptions import InvalidAnswerError, InvalidWordLengthError, WordNotFoundError
from core.language import Language, Languages, Step

import pytest


@pytest.mark.parametrize(
    "word, language",
    [
        ("code", Languages.EN),             # Word too short in English
        ("python", Languages.EN),           # Word too long in English
        ("area", Languages.ES),             # Word too short in Spanish
        ("wordle", Languages.ES),           # Word too long in Spanish
    ]
)
def test_invalid_word_length(word: str, language: Language):
    with pytest.raises(InvalidWordLengthError):
        validate_word(word, language)


@pytest.mark.parametrize(
    "word, language",
    [
        ("aaaaa", Languages.ES),            # Unknown word in Spanish
        ("aaaaa", Languages.EN),            # Unknown word in English
        ("phone", Languages.ES),            # English word in Spanish
        ("coche", Languages.EN),            # Spanish word in English
    ]
)
def test_word_not_found(word: str, language: Language):
    with pytest.raises(WordNotFoundError):
        validate_word(word, language)


@pytest.mark.parametrize(
    "answer",
    [
        ("000000"),                         # Answer too long
        ("00003"),                          # Unsupported numbers
        ("coche"),                          # Unsupported characters
    ]
)
def test_valid_answer(answer: str):
    with pytest.raises(InvalidAnswerError):
        validate_answer(answer)


@pytest.mark.parametrize(
    "steps, language",
    [
        ([                                  # Example game in Spanish
            Step(guess="careo", answer="01222"),
            Step(guess="nolit", answer="11212"),
            Step(guess="cacho", answer="02120"),
            Step(guess="cinco", answer="00000"),
        ], Languages.ES),
        ([                                  # Example game in English
            Step(guess="tares", answer="12221"),
            Step(guess="moust", answer="12211"),
            Step(guess="smith", answer="00000"),
        ], Languages.EN),
    ]
)
def test_valid_steps(steps: list[Step], language: Language):
    assert validate_steps(steps, language)

from wordlesolver.core.common import validate_answer, validate_steps, validate_word
from wordlesolver.core.exceptions import InvalidAnswerError, InvalidWordLengthError, WordNotFoundError
from wordlesolver.core.variables import Language, Languages

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
            {
                "guess" : "careo",
                "answer" : "01222",
            },
            {
                "guess" : "nolit",
                "answer" : "11212",
            },
            {
                "guess" : "cacho",
                "answer" : "02120",
            },
            {
                "guess" : "cinco",
                "answer" : "00000",
            },
        ], Languages.ES),
        ([                                  # Example game in English
            {
                "guess" : "tares",
                "answer" : "12221",
            },
            {
                "guess" : "moust",
                "answer" : "12211",
            },
            {
                "guess" : "smith",
                "answer" : "00000",
            },
        ], Languages.EN),
    ]
)
def test_valid_steps(steps: list[dict[str, str]], language: Language):
    assert validate_steps(steps, language)

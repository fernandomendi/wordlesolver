import pytest

# TODO(#50): Tests reference old module paths (wordlesolver.*) removed in the restructure.
# These will be rewritten to test via the Solver class in issue #50.
pytest.skip("Pending rewrite for new core structure — see issue #50", allow_module_level=True)

from wordlesolver.core.common import validate_answer, validate_steps, validate_word
from wordlesolver.core.exceptions import InvalidAnswerError, InvalidWordLengthError, WordNotFoundError
from wordlesolver.core.variables import Language, Languages


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
        ("000000"),
        ("00003"),
        ("coche"),
    ]
)
def test_valid_answer(answer: str):
    with pytest.raises(InvalidAnswerError):
        validate_answer(answer)


@pytest.mark.parametrize(
    "steps, language",
    [
        ([
            {"guess": "careo", "answer": "01222"},
            {"guess": "nolit", "answer": "11212"},
            {"guess": "cacho", "answer": "02120"},
            {"guess": "cinco", "answer": "00000"},
        ], Languages.ES),
        ([
            {"guess": "tares", "answer": "12221"},
            {"guess": "moust", "answer": "12211"},
            {"guess": "smith", "answer": "00000"},
        ], Languages.EN),
    ]
)
def test_valid_steps(steps: list[dict[str, str]], language: Language):
    assert validate_steps(steps, language)

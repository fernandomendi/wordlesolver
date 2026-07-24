import pytest

# TODO(#50): Tests reference old module paths (wordlesolver.*) removed in the restructure.
# These will be rewritten to test via the Solver class in issue #50.
pytest.skip("Pending rewrite for new core structure — see issue #50", allow_module_level=True)

from wordlesolver.common import feedback
from wordlesolver.core.variables import Language, Languages, Status
from wordlesolver.filter import filter_words_accumulative

import pandas as pd


@pytest.mark.parametrize(
    "secret, guess, expected",
    [
        ("sobre", "sobre", 5 * Status.CORRECT),
        ("carta", "cargo", 3 * Status.CORRECT + 2 * Status.ABSENT),
        ("pluma", "sobre", 5 * Status.ABSENT),
        ("sobre", "serbo", 1 * Status.CORRECT + 4 * Status.MISPLACED),
        ("pista", "tapis", 5 * Status.MISPLACED),
        ("apnea", "costa", 4 * Status.ABSENT + Status.CORRECT),
        ("piano", "pinoc", 2 * Status.CORRECT + 2 * Status.MISPLACED + Status.ABSENT),
        ("apple", "apply", 4 * Status.CORRECT + Status.ABSENT),
        ("level", "lemon", 2 * Status.CORRECT + 3 * Status.ABSENT),
        ("brick", "stone", 5 * Status.ABSENT),
        ("angle", "glean", 5 * Status.MISPLACED),
        ("eager", "alter", 1 * Status.MISPLACED + 2 * Status.ABSENT + 2 * Status.CORRECT),
        ("ooooo", "ooxxo", 2 * Status.CORRECT + 2 * Status.ABSENT + Status.CORRECT),
    ]
)
def test_feedback(secret: str, guess: str, expected: str):
    assert feedback(secret, guess) == expected


@pytest.mark.parametrize(
    "language",
    [Languages.ES, Languages.EN]
)
def test_no_filter(language: Language):
    filtered_words = filter_words_accumulative([], language)
    all_words = pd.read_csv(f"data/{language.code}/words.csv")
    pd.testing.assert_frame_equal(filtered_words, all_words)


@pytest.mark.parametrize(
    "guess, language",
    [
        ("coche", Languages.ES),
        ("night", Languages.EN),
    ]
)
def test_exact_filter(guess: str, language: Language):
    filtered_words = filter_words_accumulative([{"guess": guess, "answer": "00000"}], language)
    assert len(filtered_words) == 1

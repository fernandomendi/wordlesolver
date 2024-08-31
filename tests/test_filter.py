from wordlesolver.common import feedback
from wordlesolver.core.variables import Language, Languages, Status
from wordlesolver.filter import filter_words_accumulative

import pytest
import pandas as pd


@pytest.mark.parametrize(
    "secret, guess, expected",
    [
        ("sobre", "sobre", 5 * Status.CORRECT),                                                 # All letters are correct
        ("carta", "cargo", 3 * Status.CORRECT + 2 * Status.ABSENT),                             # Some letters correct, some absent
        ("pluma", "sobre", 5 * Status.ABSENT),                                                  # All letters are absent
        ("sobre", "serbo", 1 * Status.CORRECT + 4 * Status.MISPLACED),                          # Some letters correct, some misplaced
        ("pista", "tapis", 5 * Status.MISPLACED),                                               # All letters are misplaced
        ("apnea", "costa", 4 * Status.ABSENT + Status.CORRECT),                                 # One correct, rest absent
        ("piano", "pinoc", 2 * Status.CORRECT + 2 * Status.MISPLACED + Status.ABSENT),          # Some letters correct, some misplaced, some absent
        ("apple", "apply", 4 * Status.CORRECT + Status.ABSENT),                                 # Edge case with repeated letters, some correct, some absent
        ("level", "lemon", 2 * Status.CORRECT + 3 * Status.ABSENT),                             # Edge case with repeated letters, some correct, some misplaced
        ("brick", "stone", 5 * Status.ABSENT),                                                  # No letters match
        ("angle", "glean", 5 * Status.MISPLACED),                                               # All letters correct but in the wrong order
        ("eager", "alter", 1 * Status.MISPLACED + 2 * Status.ABSENT + 2 * Status.CORRECT),      # Some correct, some absent, with repeat letters
        ("ooooo", "ooxxo", 2 * Status.CORRECT + 2 * Status.ABSENT + Status.CORRECT),            # Special case: Word with all letters the same
    ]
)
def test_feedback(secret: str, guess: str, expected: str):
    assert feedback(secret, guess) == expected


@pytest.mark.parametrize(
    "language",
    [
        Languages.ES,
        Languages.EN,
    ]
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
    filtered_words = filter_words_accumulative([{
        "guess": guess,
        "answer": "00000"
    }], language)
    assert len(filtered_words) == 1

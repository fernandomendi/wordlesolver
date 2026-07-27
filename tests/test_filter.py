from core.feedback import feedback
from core.models import Language, Languages, Status
from core.data_tools import load_words
from core import Solver

import pytest


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


@pytest.mark.parametrize("language", [Languages.ES, Languages.EN])
def test_no_filter(language: Language):
    solver = Solver(language)
    assert solver.total_possible() == len(load_words(language))


@pytest.mark.parametrize(
    "guess, language",
    [
        ("coche", Languages.ES),
        ("night", Languages.EN),
    ]
)
def test_exact_filter(guess: str, language: Language):
    solver = Solver(language)
    solver.add_step(guess, "00000")
    assert solver.total_possible() == 1

from core.models import Language, Languages
from core.theory import entropy, compute_entropies
from core.data_tools import load_words

import pandas as pd
import pytest


@pytest.mark.parametrize(
    "word, value, language",
    [
        ("careo", 6.391094986076554, Languages.ES),
        ("pista", 5.538512650446942, Languages.ES),
        ("alita", 5.383778236161522, Languages.ES),
        ("tares", 6.241873393464967, Languages.EN),
        ("crane", 5.452946441848195, Languages.EN),
        ("hello", 4.515986767125182, Languages.EN),
    ]
)
def test_base_entropy(word: str, value: float, language: Language):
    all_words = load_words(language)
    assert value == entropy(word, all_words)


@pytest.mark.slow
@pytest.mark.parametrize(
    "steps, language",
    [
        ([("careo", "21222"), ("pista", "22200")], Languages.ES),
    ]
)
def test_parallelism(steps: list[tuple], language: Language):
    from core import Solver
    solver_parallel = Solver(language)
    solver_serial = Solver(language)

    for guess, answer in steps:
        solver_parallel.add_step(guess, answer)
        solver_serial.add_step(guess, answer)

    result_parallel = compute_entropies(solver_parallel._all_words, solver_parallel._possible, parallelize=True)
    result_serial = compute_entropies(solver_serial._all_words, solver_serial._possible, parallelize=False)

    pd.testing.assert_frame_equal(
        result_parallel.sort_values("id").reset_index(drop=True),
        result_serial.sort_values("id").reset_index(drop=True)
    )

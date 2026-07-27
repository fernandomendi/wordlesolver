from core.data_tools import load_words
from core.models import Language, Languages
from core.theory import compute_entropies, entropy

from math import log2
import pandas as pd
import pytest


@pytest.mark.parametrize(
    "word, expected",
    [
        ("apple", 2.5216406363433186),
        ("civic", 0.5916727785823275),
    ],
)
def test_entropy_on_fixed_fixture(word: str, expected: float):
    df_fixture_words = pd.DataFrame(
        {"word": [
            "apple",
            "allee",
            "angle",
            "amble",
            "bloom",
            "civic",
            "llama",
        ]}
    )
    assert entropy(word, df_fixture_words) == pytest.approx(expected, abs=1e-12)


@pytest.mark.parametrize("language", [Languages.ES, Languages.EN])
def test_entropy_is_deterministic_and_bounded(language: Language):
    df_words = load_words(language)
    sample_words = [df_words.iloc[0].word, df_words.iloc[len(df_words) // 2].word]

    for word in sample_words:
        value = entropy(word, df_words)
        assert value == entropy(word, df_words)
        assert 0 <= value <= log2(len(df_words))


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

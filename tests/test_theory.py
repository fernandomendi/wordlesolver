from wordlesolver.core.variables import Language, Languages
from wordlesolver.theory import best_guess, entropy, get_entropies

import pandas as pd
import pytest


@pytest.mark.parametrize(
    "word, value, language",
    [
        ("careo", 6.39140681778416, Languages.ES),
        ("pista", 5.5384429912797986, Languages.ES),
        ("alita", 5.383944162488264, Languages.ES),
        ("tares", 6.241873393464967, Languages.EN),
        ("crane", 5.452946441848195, Languages.EN),
        ("hello", 4.515986767125182, Languages.EN),
    ]
)
def test_base_entropy(word: str, value: float, language: Language):
    all_words: pd.DataFrame = pd.read_csv(f"data/{language.code}/words.csv")
    assert value == entropy(word, all_words)


@pytest.mark.skip("Takes too long (5mins) - Will resume once processing get more efficient.")
@pytest.mark.parametrize(
    "language, word",
    [
        (Languages.ES, "careo"),
        (Languages.EN, "tares"),
    ]
)
def test_most_entropy(language: Language, word: str):
    stats = get_entropies([], language)
    most_entropy = best_guess(stats, 1)

    assert most_entropy == word


@pytest.mark.parametrize(
    "steps, language",
    [
        ([                                  # Example game in Spanish
            {
                "guess" : "careo",
                "answer" : "21222",
            },
            {
                "guess" : "pista",
                "answer" : "22200",
            },
        ], Languages.ES),
    ]
)
def test_parallelism(steps: list[dict[str, str]], language: Language):
    stats_parallelism = get_entropies(steps, language, parallelize=True, recalculate=True)
    stats_basic = get_entropies(steps, language, parallelize=False, recalculate=True)

    pd.testing.assert_frame_equal(stats_parallelism, stats_basic)

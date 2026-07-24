from core.language import Language, Languages, Step
from core.theory import entropy, get_entropies
from core.filter import _load_words

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
    all_words: pd.DataFrame = _load_words(language)
    assert value == entropy(word, all_words)


@pytest.mark.skip("Takes too long (5mins) - Will resume once processing get more efficient.")
@pytest.mark.parametrize(
    "language",
    [
        (Languages.ES),
        (Languages.EN),
    ]
)
def test_most_entropy(language: Language):
    stats = get_entropies([], language)
    best = stats.sort_values("entropy", ascending=False).iloc[0]["word"]
    assert best == language.initial_suggestion


@pytest.mark.parametrize(
    "steps, language",
    [
        ([
            Step(guess="careo", answer="21222"),
            Step(guess="pista", answer="22200"),
        ], Languages.ES),
    ]
)
def test_parallelism(steps: list[Step], language: Language):
    stats_parallelism = get_entropies(steps, language, parallelize=True, recalculate=True)
    stats_basic = get_entropies(steps, language, parallelize=False, recalculate=True)

    pd.testing.assert_frame_equal(stats_parallelism, stats_basic)

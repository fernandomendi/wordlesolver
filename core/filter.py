from importlib import resources

from core.feedback import feedback
from core.models import Language, Step

import pandas as pd


def _load_words(language: Language) -> pd.DataFrame:
    with resources.files("core.data").joinpath(f"{language.code}/words.csv").open("r") as f:
        return pd.read_csv(f)


def filter_words(words: pd.DataFrame, step: Step) -> pd.DataFrame:
    if words.empty:
        return words
    filtered = words[
        words.word.apply(lambda secret: feedback(secret, step.guess) == step.answer)
    ]
    return filtered.reset_index(drop=True)

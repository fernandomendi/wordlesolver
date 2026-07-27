from core.feedback import feedback
from core.models import Step

import pandas as pd


def filter_words(words: pd.DataFrame, step: Step) -> pd.DataFrame:
    if words.empty:
        return words
    filtered = words[
        words.word.apply(lambda secret: feedback(secret, step.guess) == step.answer)
    ]
    return filtered.reset_index(drop=True)

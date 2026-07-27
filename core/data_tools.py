from __future__ import annotations

from importlib import resources
from math import exp
from pathlib import Path

import numpy as np
import pandas as pd

from core.models import Language


def sigmoid(x: float) -> float:
    return 1 / (1 + exp(-x))


def load_words_path(language: Language) -> Path:
    resource = resources.files("core.data").joinpath(f"{language.code}/words.csv")
    return Path(resource)


def rebuild_probabilities(words: pd.DataFrame) -> pd.DataFrame:
    words = words.sort_values("id").reset_index(drop=True)
    words["id"] = range(1, len(words) + 1)
    total_words = len(words)
    x_vals = np.linspace(-10, 10, total_words)
    words["probability"] = words["id"].apply(lambda x: sigmoid(x_vals[total_words - x]))
    return words


def normalize_word(word: str) -> str:
    return word.strip().lower()

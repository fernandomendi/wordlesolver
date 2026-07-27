from __future__ import annotations

from importlib import resources
from math import exp
from pathlib import Path
from tempfile import NamedTemporaryFile

import numpy as np
import pandas as pd

from core.models import Language


def sigmoid(x: float) -> float:
    return 1 / (1 + exp(-x))


def load_words_path(language: Language) -> Path:
    resource = resources.files("core.data").joinpath(f"{language.code}/words.txt")
    return Path(resource)


def normalize_word(word: str) -> str:
    return word.strip().lower()


def load_word_list(language: Language) -> list[str]:
    words_path = load_words_path(language)
    with words_path.open("r", encoding="utf-8") as handle:
        raw_lines = [line.rstrip("\n") for line in handle]

    if any(not line.strip() for line in raw_lines):
        raise ValueError(f"Invalid word list entry in {words_path}: blank line.")

    words = [normalize_word(line) for line in raw_lines]

    invalid_words = [word for word in words if len(word) != 5 or not word.isalpha()]
    if invalid_words:
        raise ValueError(f"Invalid word list entry in {words_path}: {invalid_words[0]!r}")
    if len(set(words)) != len(words):
        raise ValueError(f"Invalid word list entry in {words_path}: duplicate word.")

    return words


def load_words(language: Language) -> pd.DataFrame:
    # Load language words as list
    words = load_word_list(language)

    # Create rank for each word
    df_words = pd.DataFrame({"word": words})
    df_words["id"] = range(1, len(df_words) + 1)

    # Calculate probability for each word using a sigmoid function
    total_words = len(df_words)
    sigmoid_domain = np.linspace(-10, 10, total_words)
    df_words["probability"] = df_words["id"].apply(
        lambda rank: sigmoid(sigmoid_domain[total_words - rank])
    )

    return df_words


def write_words(path: Path, words: list[str]) -> None:
    with NamedTemporaryFile("w", encoding="utf-8", delete=False, dir=path.parent) as handle:
        temp_path = Path(handle.name)
        handle.write("\n".join(words))
        handle.write("\n" if words else "")
    temp_path.replace(path)

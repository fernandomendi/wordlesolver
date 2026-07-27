from __future__ import annotations

import argparse
import shutil
import sys
from importlib import resources
from math import exp
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from core.models import Languages, Language


def sigmoid(x: float) -> float:
    return 1 / (1 + exp(-x))


def get_language(code: str) -> Language:
    match code.lower():
        case "en":
            return Languages.EN
        case "es":
            return Languages.ES
        case _:
            raise ValueError("Language must be 'en' or 'es'.")


def load_words_path(language: Language) -> Path:
    resource = resources.files("core.data").joinpath(f"{language.code}/words.csv")
    return Path(resource)


def rebuild_probabilities(words: pd.DataFrame) -> pd.DataFrame:
    words = words.sort_values("id").reset_index(drop=True)
    total_words = len(words)
    x_vals = np.linspace(-10, 10, total_words)
    words["probability"] = words["id"].apply(lambda x: sigmoid(x_vals[total_words - x]))
    return words


def clear_cache() -> None:
    cache_path = Path(__file__).resolve().parents[1] / ".cache"
    if cache_path.exists():
        shutil.rmtree(cache_path)


def add_word(word: str, language: Language) -> None:
    words_path = load_words_path(language)
    words = pd.read_csv(words_path)

    normalized = word.strip().lower()
    if len(normalized) != 5 or not normalized.isascii() or not normalized.isalpha():
        raise ValueError("Word must be exactly 5 ASCII letters.")

    if any(words.word == normalized):
        raise ValueError(f"'{normalized}' is already in the {language.code} word list.")

    next_id = int(words.id.max()) + 1
    words = pd.concat(
        [
            words,
            pd.DataFrame([{"id": next_id, "word": normalized}]),
        ],
        ignore_index=True,
    )
    words = rebuild_probabilities(words)
    words.to_csv(words_path, index=False)
    clear_cache()


def main() -> None:
    parser = argparse.ArgumentParser(description="Add a word to a Wordle word list.")
    parser.add_argument("word", help="Word to add to the word list.")
    parser.add_argument("language", choices=["en", "es"], help="Target language.")
    args = parser.parse_args()

    language = get_language(args.language)
    add_word(args.word, language)
    print(f"Added '{args.word.lower()}' to {language.code} word list.")


if __name__ == "__main__":
    main()

from __future__ import annotations

import argparse
import sys

import pandas as pd

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from core import cache
from core.data_tools import load_words_path, normalize_word, rebuild_probabilities
from core.models import Language
from core.parsing import parse_language


def add_word(word: str, language: Language) -> None:
    words_path = load_words_path(language)
    words = pd.read_csv(words_path).sort_values("id").reset_index(drop=True)

    normalized = normalize_word(word)
    if len(normalized) != 5 or not normalized.isascii() or not normalized.isalpha():
        raise ValueError("Word must be exactly 5 ASCII letters.")

    if any(words.word == normalized):
        raise ValueError(f"'{normalized}' is already in the {language.code} word list.")

    next_id = int(words.id.max()) + 1
    words = pd.concat([words, pd.DataFrame([{"id": next_id, "word": normalized}])], ignore_index=True)
    words = rebuild_probabilities(words)
    words.to_csv(words_path, index=False)
    cache.clear()


def main() -> None:
    parser = argparse.ArgumentParser(description="Add a word to a Wordle word list.")
    parser.add_argument("word", help="Word to add to the word list.")
    parser.add_argument("language", help="Target language.")
    args = parser.parse_args()

    language = parse_language(args.language)
    add_word(args.word, language)
    print(f"Added '{args.word.lower()}' to {language.code} word list.")


if __name__ == "__main__":
    main()

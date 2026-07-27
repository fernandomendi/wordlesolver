"""Remove a word from a language word list and rebuild derived probabilities."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from core import cache
from core.data_tools import load_word_list, load_words_path, normalize_word, write_words
from core.models import Language
from core.parsing import parse_language


def remove_word(language: Language, word: str) -> None:
    words_path = load_words_path(language)
    words = load_word_list(language)

    normalized = normalize_word(word)
    if len(normalized) != 5 or not normalized.isalpha():
        raise ValueError("Word must be exactly 5 letters.")

    if normalized not in words:
        raise ValueError(f"'{normalized}' is not in the {language.code} word list.")

    filtered = [entry for entry in words if entry != normalized]
    write_words(words_path, filtered)
    cache.clear()


def main() -> None:
    parser = argparse.ArgumentParser(description="Remove a word from a Wordle word list.")
    parser.add_argument("language", help="Target language.")
    parser.add_argument("word", help="Word to remove from the word list.")
    args = parser.parse_args()

    language = parse_language(args.language)
    remove_word(language, args.word)
    print(f"Removed '{args.word.lower()}' from {language.code} word list.")


if __name__ == "__main__":
    main()

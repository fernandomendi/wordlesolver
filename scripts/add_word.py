"""Add a word to a language word list and rebuild derived probabilities."""

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


def add_word(language: Language, word: str, rank: int | None = None) -> None:
    words_path = load_words_path(language)
    words = load_word_list(language)

    normalized = normalize_word(word)
    if len(normalized) != 5 or not normalized.isalpha():
        raise ValueError("Word must be exactly 5 letters.")

    if normalized in words:
        raise ValueError(f"'{normalized}' is already in the {language.code} word list.")

    if rank is not None and not 1 <= rank <= len(words) + 1:
        raise ValueError(f"Rank must be between 1 and {len(words) + 1}.")

    insert_at = len(words) if rank is None else rank - 1
    words.insert(insert_at, normalized)
    write_words(words_path, words)
    cache.clear()


def main() -> None:
    parser = argparse.ArgumentParser(description="Add a word to a Wordle word list.")
    parser.add_argument("language", help="Target language.")
    parser.add_argument("word", help="Word to add to the word list.")
    parser.add_argument(
        "--rank",
        type=int,
        default=None,
        help="Optional 1-based insertion rank. Existing entries are shifted down.",
    )
    args = parser.parse_args()

    language = parse_language(args.language)
    add_word(language, args.word, rank=args.rank)
    if args.rank is None:
        print(f"Added '{args.word.lower()}' to {language.code} word list.")
    else:
        print(f"Added '{args.word.lower()}' at rank {args.rank} in {language.code} word list.")


if __name__ == "__main__":
    main()

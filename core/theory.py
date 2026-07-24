from math import log2
from functools import reduce
import os
import multiprocessing as mp
from pathlib import Path

from core.filter import filter_words_accumulative, _load_words
from core.feedback import feedback
from core.language import Language, Step
from core.validations import validate_steps

import pandas as pd

CACHE_DIR = Path(".cache")


def entropy(word: str, words: pd.DataFrame) -> float:
    words_aux = words.copy()
    words_count = len(words_aux)

    words_aux["answer"] = words_aux.word.apply(lambda x: feedback(word, x))

    answer_frequencies = words_aux.answer.value_counts()
    answer_probabilities = answer_frequencies / words_count

    return -reduce(
        lambda acc, prob: acc + prob * log2(prob),
        answer_probabilities,
        0
    )


def _process_entropies_chunk(chunk: pd.DataFrame, possible_words: pd.DataFrame) -> pd.DataFrame:
    chunk["entropy"] = chunk.word.apply(lambda word: entropy(word, possible_words))
    return chunk


def _split_chunks(df: pd.DataFrame, n_chunks: int) -> list[pd.DataFrame]:
    chunks = []
    accumulate_rows = 0
    row_count = len(df)
    base_chunk_size = row_count // n_chunks
    remaining_rows = row_count % n_chunks

    for i in range(n_chunks):
        chunk_size = base_chunk_size + (i < remaining_rows)
        chunks.append(df.iloc[accumulate_rows: accumulate_rows + chunk_size])
        accumulate_rows += chunk_size

    return chunks


def get_entropies(
        steps: list[Step],
        language: Language,
        parallelize: bool = True,
        recalculate: bool = False
    ) -> pd.DataFrame:

    validate_steps(steps, language)

    all_words = _load_words(language)

    cache_path = CACHE_DIR / language.code / "/".join(
        f"guess={s.guess}/answer={s.answer}" for s in steps
    )

    if recalculate and (cache_path / "stats.csv").exists():
        (cache_path / "stats.csv").unlink()

    if (cache_path / "stats.csv").exists():
        cache = pd.read_csv(cache_path / "stats.csv")
        return pd.merge(all_words, cache, on="id")

    possible_words = filter_words_accumulative(steps, language)
    words_aux = all_words.copy()

    if parallelize:
        n_processes = mp.cpu_count() // 2
        chunks = _split_chunks(words_aux, n_processes)
        with mp.Pool(processes=n_processes) as pool:
            stats_chunks = pool.starmap(
                _process_entropies_chunk,
                [(chunk, possible_words) for chunk in chunks]
            )
        stats = pd.concat(stats_chunks)
    else:
        words_aux["entropy"] = words_aux.word.apply(
            lambda word: entropy(word, possible_words)
        )
        stats = words_aux

    cache_path.mkdir(parents=True, exist_ok=True)
    stats[["id", "entropy"]].to_csv(cache_path / "stats.csv", index=False)

    return stats

from math import log2
from functools import reduce
import multiprocessing as mp

from core.feedback import feedback

import pandas as pd


def entropy(word: str, possible_words: pd.DataFrame) -> float:
    counts = possible_words.word.apply(lambda secret: feedback(word, secret)).value_counts()
    probabilities = counts / len(possible_words)
    return -reduce(lambda acc, p: acc + p * log2(p), probabilities, 0)


def _compute_chunk(chunk: pd.DataFrame, possible_words: pd.DataFrame) -> pd.DataFrame:
    chunk = chunk.copy()
    chunk["entropy"] = chunk.word.apply(lambda word: entropy(word, possible_words))
    return chunk


def _split_chunks(df: pd.DataFrame, n: int) -> list[pd.DataFrame]:
    size = len(df)
    base, remainder = divmod(size, n)
    chunks, i = [], 0
    for k in range(n):
        chunk_size = base + (1 if k < remainder else 0)
        chunks.append(df.iloc[i:i + chunk_size])
        i += chunk_size
    return chunks


def compute_entropies(all_words: pd.DataFrame, possible_words: pd.DataFrame, parallelize: bool = True) -> pd.DataFrame:
    if parallelize:
        n = mp.cpu_count() // 2
        chunks = _split_chunks(all_words.copy(), n)
        with mp.Pool(processes=n) as pool:
            results = pool.starmap(_compute_chunk, [(c, possible_words) for c in chunks])
        return pd.concat(results)

    result = all_words.copy()
    result["entropy"] = result.word.apply(lambda word: entropy(word, possible_words))
    return result

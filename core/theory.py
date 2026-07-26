from math import log2
from functools import reduce
import multiprocessing as mp

import pandas as pd

from core.feedback import feedback


def entropy(word: str, possible_words: pd.DataFrame) -> float:
    counts = possible_words.word.apply(lambda secret: feedback(word, secret)).value_counts()
    probabilities = counts / len(possible_words)
    return -reduce(lambda acc, p: acc + p * log2(p), probabilities, 0)


def _compute_chunk(chunk: pd.DataFrame, possible_words: pd.DataFrame) -> pd.DataFrame:
    chunk = chunk.copy()
    chunk["entropy"] = chunk.word.apply(lambda word: entropy(word, possible_words))
    return chunk


def compute_entropies(all_words: pd.DataFrame, possible_words: pd.DataFrame, parallelize: bool = True) -> pd.DataFrame:
    if parallelize:
        n = mp.cpu_count() // 2
        df = all_words.copy()
        chunks = [df.iloc[i::n] for i in range(n)]
        with mp.Pool(processes=n) as pool:
            results = pool.starmap(_compute_chunk, [(c, possible_words) for c in chunks])
        return pd.concat(results)

    result = all_words.copy()
    result["entropy"] = result.word.apply(lambda word: entropy(word, possible_words))
    return result

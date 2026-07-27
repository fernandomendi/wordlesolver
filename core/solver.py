from core import cache
from core.data_tools import load_words
from core.filter import filter_words
from core.theory import compute_entropies
from core.models import Language, Step
from core.validations import validate_word, validate_answer

import pandas as pd


class Solver:
    def __init__(self, language: Language):
        self._language = language
        self._steps: list[Step] = []
        self._all_words: pd.DataFrame = load_words(language)
        self._possible: pd.DataFrame = self._all_words.copy()
        self._entropies: pd.DataFrame | None = None

    def add_step(self, guess: str, answer: str) -> None:
        validate_word(guess, self._language)
        validate_answer(answer)
        step = Step(guess=guess, answer=answer)
        self._steps.append(step)
        self._possible = filter_words(self._possible, step)
        self._entropies = None

    def _get_entropies(self) -> pd.DataFrame:
        if self._entropies is not None:
            return self._entropies

        cached = cache.read(self._language, self._steps)
        if cached is not None:
            self._entropies = pd.merge(self._all_words, cached, on="id")
            return self._entropies

        result = compute_entropies(self._all_words, self._possible)
        cache.write(self._language, self._steps, result[["id", "entropy"]])
        self._entropies = result
        return self._entropies

    def _ranked(self) -> pd.DataFrame:
        stats = self._get_entropies().copy()
        n = len(self._possible)

        stats["entropy_norm"] = (
            (stats.entropy - stats.entropy.min())
            / (stats.entropy.max() - stats.entropy.min())
        )

        possible_ids = set(self._possible["id"])
        stats["is_possible"] = stats["id"].apply(lambda x: 1 if x in possible_ids else 0)

        # Shift weighting as search space shrinks: early game favors entropy exploration,
        # later game favors probability exploitation.
        threshold = len(stats) if not self._steps else self._language.threshold
        ratio = n / threshold
        entropy_weight = 0.2 + 0.6 * ratio

        stats["guessability"] = (
            entropy_weight * stats["entropy_norm"]
            + (1 - entropy_weight) * stats["probability"]
            + stats["is_possible"] / n
        )

        return stats.sort_values("guessability", ascending=False).reset_index(drop=True)

    def possible_words(self) -> list[dict]:
        return self._possible.head(10).to_dict(orient="records")

    def total_possible(self) -> int:
        return len(self._possible)

    def best_guess(self) -> str:
        return self._ranked().loc[0, "word"]

    def suggestions(self) -> list[dict]:
        return self._ranked().head(10)[["word", "guessability"]].to_dict(orient="records")

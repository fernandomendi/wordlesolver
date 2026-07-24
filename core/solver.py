from core.filter import filter_words_accumulative, _load_words
from core.theory import get_entropies
from core.language import Language, Step

import pandas as pd


class Solver:
    def __init__(self, language: Language):
        self._language = language
        self._steps: list[Step] = []
        self._words: pd.DataFrame = _load_words(language)

    def add_step(self, guess: str, answer: str) -> None:
        self._steps.append(Step(guess=guess, answer=answer))

    def possible_words(self) -> list[dict]:
        words = filter_words_accumulative(self._steps, self._language)
        return words.head(10).to_dict(orient="records")

    def total_possible(self) -> int:
        return len(filter_words_accumulative(self._steps, self._language))

    def best_guess(self) -> str:
        return self._ranked_suggestions().loc[0, "word"]

    def suggestions(self) -> list[dict]:
        return (
            self._ranked_suggestions()
            .head(10)[["word", "guessability"]]
            .to_dict(orient="records")
        )

    def _ranked_suggestions(self) -> pd.DataFrame:
        stats = get_entropies(self._steps, self._language)
        possible = filter_words_accumulative(self._steps, self._language)

        n_words_left = len(possible)

        stats["entropy_norm"] = (
            (stats.entropy - stats.entropy.min())
            / (stats.entropy.max() - stats.entropy.min())
        )

        possible["is_possible"] = 1
        stats_ext = pd.merge(stats, possible[["id", "is_possible"]], on="id", how="left")
        stats_ext.is_possible = stats_ext.is_possible.fillna(0)

        threshold = len(stats) if len(self._steps) == 0 else self._language.threshold
        ratio = n_words_left / threshold
        entropy_weight = 0.2 + 0.6 * ratio

        stats_ext["guessability"] = stats_ext.apply(
            lambda row: (
                entropy_weight * row.entropy_norm
                + (1 - entropy_weight) * row.probability
            ) + row.is_possible / n_words_left,
            axis=1
        )

        return stats_ext.sort_values("guessability", ascending=False).reset_index()

from importlib import resources

from core.feedback import feedback
from core.language import Language, Step
from core.validations import validate_answer, validate_word

import pandas as pd


def _load_words(language: Language) -> pd.DataFrame:
    with resources.files("core.data").joinpath(f"{language.code}/words.csv").open("r") as f:
        return pd.read_csv(f)


def filter_words(words: pd.DataFrame, step: Step, language: Language) -> pd.DataFrame:
    validate_word(step.guess, language)
    validate_answer(step.answer)

    filtered = words[
        words.word.apply(lambda secret: feedback(secret, step.guess) == step.answer)
    ]

    return filtered.reset_index(drop=True)


def filter_words_accumulative(steps: list[Step], language: Language) -> pd.DataFrame:
    match len(steps):
        case 0:
            return _load_words(language)
        case 1:
            words = _load_words(language)
            return filter_words(words, steps[0], language)
        case _:
            possible_words = filter_words_accumulative(steps[:-1], language)
            return filter_words(possible_words, steps[-1], language)

from collections.abc import Mapping, Sequence

from core.models import Language, Languages, Step


def parse_language(language_code: object) -> Language:
    if not isinstance(language_code, str):
        raise ValueError("'language' is required and must be a string.")

    languages = {
        "en": Languages.EN,
        "es": Languages.ES,
    }
    language = languages.get(language_code.lower())
    if language is None:
        raise ValueError(f"Unsupported language '{language_code}'. Use 'en' or 'es'.")

    return language


def parse_steps(raw_steps: object) -> list[Step]:
    if raw_steps is None:
        return []
    if isinstance(raw_steps, (str, bytes)) or not isinstance(raw_steps, Sequence):
        raise ValueError("'steps' must be a list.")

    parsed_steps: list[Step] = []
    for index, raw_step in enumerate(raw_steps):
        parsed_steps.append(_parse_step(raw_step, index))

    return parsed_steps


def _parse_step(raw_step: object, index: int) -> Step:
    if isinstance(raw_step, Step):
        return raw_step

    if isinstance(raw_step, Mapping):
        guess = raw_step.get("guess")
        answer = raw_step.get("answer")
    elif isinstance(raw_step, Sequence) and not isinstance(raw_step, (str, bytes)):
        if len(raw_step) != 2:
            raise ValueError(f"'steps[{index}]' must contain exactly 2 items.")
        guess, answer = raw_step
    else:
        raise ValueError(f"'steps[{index}]' must be an object or pair.")

    if not isinstance(guess, str):
        raise ValueError(f"'steps[{index}].guess' must be a string.")
    if not isinstance(answer, str):
        raise ValueError(f"'steps[{index}].answer' must be a string.")

    return Step(guess=guess, answer=answer)

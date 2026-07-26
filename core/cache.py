import hashlib
from pathlib import Path

from core.models import Language, Step

import pandas as pd

CACHE_DIR = Path(".cache")


def _key(language: Language, steps: list[Step]) -> str:
    raw = language.code + ":" + "|".join(f"{s.guess}:{s.answer}" for s in steps)
    return hashlib.md5(raw.encode()).hexdigest()


def read(language: Language, steps: list[Step]) -> pd.DataFrame | None:
    path = CACHE_DIR / f"{_key(language, steps)}.csv"
    return pd.read_csv(path) if path.exists() else None


def write(language: Language, steps: list[Step], data: pd.DataFrame) -> None:
    CACHE_DIR.mkdir(exist_ok=True)
    data.to_csv(CACHE_DIR / f"{_key(language, steps)}.csv", index=False)

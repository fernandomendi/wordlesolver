from dataclasses import dataclass


@dataclass(frozen=True)
class Language:
    code: str
    threshold: int


@dataclass
class Step:
    guess: str
    answer: str


class Languages:
    ES: Language = Language(code="es", threshold=520)
    EN: Language = Language(code="en", threshold=858)


class Status:
    CORRECT: str = "0"
    MISPLACED: str = "1"
    ABSENT: str = "2"

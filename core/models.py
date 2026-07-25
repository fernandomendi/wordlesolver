from dataclasses import dataclass


@dataclass(frozen=True)
class Language:
    code: str
    initial_suggestion: str
    threshold: int


@dataclass
class Step:
    guess: str
    answer: str


class Languages:
    ES: Language = Language(
        code="es",
        initial_suggestion="careo",
        threshold=520
    )
    EN: Language = Language(
        code="en",
        initial_suggestion="tares",
        threshold=858
    )

    def from_code(self, language_name: str) -> Language:
        return getattr(self, language_name)


class Status:
    CORRECT: str = "0"
    MISPLACED: str = "1"
    ABSENT: str = "2"

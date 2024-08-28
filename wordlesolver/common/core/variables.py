class Language:
    def __init__(self, code, best_initial_guess):
        self.code = code
        self.best_initial_guess = best_initial_guess

    def __repr__(self):
        return self.code.upper()


class Languages:
    ES: Language = Language(
        code = "es",
        best_initial_guess = "careo"
    )
    EN: Language = Language(
        code = "en",
        best_initial_guess = "tares"
    )

    def from_code(self, language_name: str) -> Language:
        return getattr(self, language_name)


class Status:
    """
    A class to represent the status of a letter in a Wordle guess.
    
    This class provides predefined instances of Status for each possible outcome:
    CORRECT, MISPLACED, and ABSENT.
    
    Attributes:
    ----------
    CORRECT : str
        Represents a letter that is in the correct position ('0').
    MISPLACED : str
        Represents a letter that is in the word but in the wrong position ('1').
    ABSENT : str
        Represents a letter that is not in the word at all ('2').
    """

    CORRECT: str = "0"
    MISPLACED: str = "1"
    ABSENT: str = "2"

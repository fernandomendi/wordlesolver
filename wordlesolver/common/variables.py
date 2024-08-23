class Language:
    """
    A class to represent language codes.

    This class provides predefined string constants for supported languages, making it easier 
    to reference and manage language settings across the application.

    Attributes:
    ----------
    ES : str
        Represents the Spanish language code ('es').
    EN : str
        Represents the English language code ('en').
    """
    ES: str = "es"
    EN: str = "en"


class Status:
    """
    A class to represent the status of a letter in a Wordle guess.

    Attributes:
    ----------
    code : str
        A string representing the status code ('0' for correct, '1' for misplaced, '2' for absent).
    color : str
        A string representing the color associated with the status, typically used for UI display in hexadecimal format.
    """
    def __init__(self, code: str, color: str):
        self.code: str = code
        self.color: str = color

    def __repr__(self):
        return f"{self.code} : #{self.color}"


class Answer:
    """
    A class that holds the possible statuses for letters in a Wordle guess.
    
    This class provides predefined instances of Status for each possible outcome:
    CORRECT, MISPLACED, and ABSENT.
    
    Attributes:
    ----------
    CORRECT : Status
        Represents a letter that is in the correct position ('0') and is colored green ('#43a047').
    MISPLACED : Status
        Represents a letter that is in the word but in the wrong position ('1') and is colored yellow ('#e4a81d').
    ABSENT : Status
        Represents a letter that is not in the word at all ('2') and is colored gray ('#757575').
    """
    CORRECT: Status = Status("0", "43a047")
    MISPLACED: Status = Status("1", "e4a81d")
    ABSENT: Status = Status("2", "757575")

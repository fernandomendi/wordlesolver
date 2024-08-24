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


def reformat_answer(answer: str) -> list[str]:
    status_list = []
    for code in answer:
        match code:
            case "0":
                status_list.append(Status.CORRECT)
            case "1":
                status_list.append(Status.MISPLACED)
            case "2":
                status_list.append(Status.ABSENT)

    return status_list

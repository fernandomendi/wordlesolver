from dataclasses import dataclass


@dataclass(frozen=True)
class Language:
    """
    A class to represent a language configuration used in the word-guessing game.

    Attributes
    ----------
    code : str
        The language code (e.g., "es" for Spanish, "en" for English).
    initial_suggestion : str
        The best initial word guess for the language, typically chosen based on frequency analysis or other heuristic.
    """

    code: str
    initial_suggestion: str
    threshold: int


class Languages:
    """
    A class that holds different Language configurations and provides methods to retrieve them.

    Attributes
    ----------
    ES : Language
        A Language object for Spanish ("es"), with a predefined best initial guess.
    EN : Language
        A Language object for English ("en"), with a predefined best initial guess.
    """

    ES: Language = Language(
        code = "es",
        initial_suggestion = "careo",
        threshold = 520
    )
    EN: Language = Language(
        code = "en",
        initial_suggestion = "tares",
        threshold = 858
    )

    def from_code(self, language_name: str) -> Language:
        """
        Retrieve the Language object based on a language code string.

        Parameters
        ----------
        language_name : str
            The language code as a string (e.g., "ES" for Spanish, "EN" for English).

        Returns
        -------
        Language
            The Language object corresponding to the provided language code.

        Raises
        ------
        AttributeError
            If the language code does not match any of the predefined languages, an AttributeError is raised.
        """

        # Use getattr to dynamically access the Language attribute based on the string provided.
        # This allows the method to retrieve the corresponding Language object by code (e.g., "ES", "EN").
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

from wordlesolver.common.core.variables import Language


class InvalidWordLengthError(Exception):
    """Exception raised when a word is not exactly 5 letters long."""
    def __init__(self, word: str):
        self.word = word
        self.length = len(word)
        self.message = f"The word '{word}' is {self.length} characters long. It must be exactly 5 characters long."
        super().__init__(self.message)


class WordNotFoundError(Exception):
    """Exception raised when a word is not found in the word list."""
    def __init__(self, word: str, language: Language):
        self.word = word
        self.language = language
        self.message = f"The word '{word}' does not exist in the {language} word list."
        super().__init__(self.message)


class InvalidAnswerError(Exception):
    """Exception raised when an answer string is not a valid Wordle-style answer."""
    def __init__(self, answer: str):
        self.answer = answer
        self.message = f"The answer '{answer}' is not a valid Wordle-style answer. It must be exactly 5 characters long, with each character being '0', '1', or '2'."
        super().__init__(self.message)


class InvalidLanguageError(Exception):
    """Exception raised for invalid language input."""
    def __init__(self, language: str):
        self.language = language
        self.message = f"'{self.language}' is not a supported language."
        super().__init__(self.message)

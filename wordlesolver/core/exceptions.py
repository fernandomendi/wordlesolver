from wordlesolver.core.variables import Language


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


class InvalidWeightError(Exception):
    """Exception raised when a weight is not a value between 0 and 1."""
    def __init__(self, weight: float):
        self.weight = weight
        self.message = f"The value '{weight}' is not a valid guess weight. It must be a value between 0 and 1."
        super().__init__(self.message)

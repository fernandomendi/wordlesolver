from core.models import Language


class InvalidWordLengthError(Exception):
    def __init__(self, word: str):
        self.word = word
        self.length = len(word)
        self.message = f"The word '{word}' is {self.length} characters long. It must be exactly 5 characters long."
        super().__init__(self.message)


class WordNotFoundError(Exception):
    def __init__(self, word: str, language: Language):
        self.word = word
        self.language = language
        self.message = f"The word '{word}' does not exist in the {language} word list."
        super().__init__(self.message)


class InvalidAnswerError(Exception):
    def __init__(self, answer: str):
        self.answer = answer
        self.message = f"The answer '{answer}' is not a valid Wordle-style answer. It must be exactly 5 characters long, with each character being '0', '1', or '2'."
        super().__init__(self.message)

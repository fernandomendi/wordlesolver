from common.variables import Status, Answer
import pandas as pd

def feedback(secret: str, guess: str) -> list[Status]:
    """
    Evaluates a Wordle guess against a secret word and returns a string representing the feedback for each letter in the guess. The feedback is provided as a sequence of status codes, where each code corresponds to the status of a letter in the guess:
    
    The function operates in two passes:
    1. It first identifies all letters that are in the correct position.
    2. Then, it identifies any letters that are in the word but in the wrong position.

    Parameters:
    ----------
    secret : str
        The secret word against which the guess is evaluated. It should be a 5-letter string.
    guess : str
        The guessed word that needs to be evaluated. It should be a 5-letter string.

    Returns:
    -------
    list[Status]
        A list of Status objects representing the status of each letter in the guess. The list contains five Status objects, each corresponding to one letter in the guess.
    """

    # Initialize the answer with a list of ABSENT Status objects
    answer = [Answer.ABSENT] * 5

    # First pass: Identify correct positions
    for i in range(5):
        if guess[i] == secret[i]:
            answer[i] = Answer.CORRECT
            secret = secret[:i] + '_' + secret[i+1:]

    # Second pass: Identify misplaced letters
    for i in range(5):
        if answer[i] == Answer.ABSENT and guess[i] in secret:
            answer[i] = Answer.MISPLACED
            secret = secret.replace(guess[i], "_", 1)

    return answer

def possible_words(words: pd.DataFrame, guess: str, answer: list[Status]) -> pd.DataFrame:
    """
    Filters the words dataframe to find words that match the given guess and expected feedback.

    Parameters:
    ----------
    words : pd.DataFrame
        DataFrame containing a column 'word' with possible words.
    guess : str
        The guessed word to be used for comparison. It should be a 5-letter string.
    answer : list[Status]
        List of Status objects representing the expected feedback for the guess.

    Returns:
    -------
    pd.DataFrame
        A DataFrame containing only the words that match the given feedback.
    """

    # Apply the feedback function and filter based on the expected answer
    filtered_words = words[
        words.word.apply(
            lambda secret: feedback(secret, guess) == answer
        )
    ]

    return filtered_words

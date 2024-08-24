from math import log2
import pandas as pd

from common.variables import Status


def feedback(secret: str, guess: str) -> list[str]:
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
    list[str]
        A list of str objects representing the status of each letter in the guess. The list contains five str objects, each corresponding to one letter in the guess.
    """

    # Initialize the answer with a list of ABSENT Status objects
    answer = [Status.ABSENT] * 5

    # First pass: Identify correct positions
    for i in range(5):
        if guess[i] == secret[i]:
            answer[i] = Status.CORRECT
            secret = secret[:i] + '_' + secret[i+1:]

    # Second pass: Identify misplaced letters
    for i in range(5):
        if answer[i] == Status.ABSENT and guess[i] in secret:
            answer[i] = Status.MISPLACED
            secret = secret.replace(guess[i], "_", 1)

    return answer

def filter_words(words: pd.DataFrame, guess: str, answer: list[str]) -> pd.DataFrame:
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

    return filtered_words.reset_index(drop=True)

def entropy(word: str, words: pd.DataFrame) -> float:
    """
    Calculates the entropy of a given word based on a set of possible words.

    Entropy is a measure of uncertainty or information content. In this context, it quantifies the uncertainty of the feedback (in terms of correct, misplaced, and absent letters) that the word would generate when guessed against all possible words.

    Parameters:
    ----------
    word : str
        The 5-letter word for which the entropy is being calculated. 
    words : pd.DataFrame
        A DataFrame containing a column 'word' with possible words to compare against. Each word in this DataFrame is considered as a potential guess.

    Returns:
    -------
    float
        The entropy value of the given word. Higher entropy indicates greater uncertainty in the feedback distribution, meaning the word could generate a wide variety of feedback patterns against the possible words.

    Process:
    -------
    1. For each word in the `words` DataFrame, calculate the feedback pattern (as a `Status` list) when guessing the `word` against each possible word.
    2. Convert each feedback pattern into a string code using the `word_code` function.
    3. Count the occurrences of each unique feedback pattern (using a dictionary to store frequencies).
    4. Calculate the entropy by summing up `-frequency * log2(frequency)` for each unique feedback pattern.

    Example:
    -------
    If the possible words are ["apple", "apply", "ample"], and the word being evaluated is "apple", the function will compute the feedback for "apple" against each word in the list, determine the frequency of each feedback pattern, and then calculate the entropy based on these frequencies.
    """

    # Dictionary to store the frequency of each unique feedback pattern
    answer_frequencies: dict = {}

    # Iterate over each word in the DataFrame and calculate feedback
    for _, row in words.iterrows():
        guess: str = row["word"]
        answer: list[str] = feedback(word, guess)
        answer_code: str = "".join(answer)

        # Update the frequency count for the current feedback pattern
        if answer_code not in answer_frequencies:
            answer_frequencies[answer_code] = 1
        else:
            answer_frequencies[answer_code] += 1

    # Calculate entropy based on the frequency distribution of feedback patterns
    entropy_sum: float = 0
    words_count: int = len(words)
    for _, frequency in answer_frequencies.items():
        probability = frequency / words_count
        entropy_sum -= probability * log2(probability)

    return entropy_sum

def calculate_entropies(all_words: pd.DataFrame, possible_words: pd.DataFrame):
    """
    Calculate the entropy for each word in the provided list of all possible words, 
    based on how that word would perform as a guess against the list of possible remaining words.

    Parameters:
    -----------
    all_words : pd.DataFrame
        A DataFrame containing the complete list of words, typically representing all valid guesses.
    possible_words : pd.DataFrame
        A DataFrame containing the subset of words that are still considered possible based on previous guesses.

    Returns:
    --------
    pd.DataFrame
        A DataFrame with the original words from `all_words`, with an additional column 'entropy' that contains the calculated entropy value for each word.

    Notes:
    ------
    - The `progress_apply` method is used to apply the `entropy` function to each word, with a progress bar for better tracking.
    - The higher the entropy of a word, the more it is expected to help in narrowing down the set of possible remaining words.
    """

    # Create a copy of the all_words DataFrame to work with, avoiding modifications to the original DataFrame.
    words_aux: pd.DataFrame = all_words

    # Calculate entropy for each word in all_words by applying the entropy function.

    words_aux["entropy"] = words_aux.word.progress_apply(
        lambda word: entropy(word, possible_words)
    )

    return words_aux


def best_guess(words: pd.DataFrame, weight: float) -> str:
    """
    Determines the best word to guess based on a weighted average of entropy and probability.

    The function calculates a new column called 'guessability' for each word, which is a weighted average of the entropy and probability columns. The word with the highest guessability score is then selected as the best guess.

    Parameters:
    ----------
    words : pd.DataFrame
        A DataFrame containing a column 'word', along with 'entropy' and 'probability' columns for each word.
    weight : float
        A floating-point value between 0 and 1 representing the weight of the entropy in the weighted average.
        - A weight closer to 1 gives more importance to entropy.
        - A weight closer to 0 gives more importance to probability.

    Returns:
    -------
    str
        The word with the highest guessability score, which is considered the best guess.

    Raises:
    ------
    ValueError
        If the weight is not between 0 and 1, a ValueError is raised.
    """

    # Ensure the weight is a number between 0 and 1
    if weight < 0 or weight > 1:
        raise ValueError("The weight must be between 0 and 1.")

    # Calculate the 'guessability' score as a weighted average of entropy and probability
    words["guessability"] = weight * words.entropy + (1 - weight) * words.probability

    # Find the word with the highest 'guessability' score
    guess: str = words \
        .sort_values("guessability", ascending=False) \
        .reset_index() \
        .loc[0, "word"]

    return guess

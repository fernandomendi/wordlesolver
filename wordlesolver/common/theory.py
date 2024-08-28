from math import log2
from functools import reduce
import os
import multiprocessing as mp

from wordlesolver.common.core.utilities import split_chunks
from wordlesolver.common.core.variables import Language, Status
from wordlesolver.common import query
from wordlesolver.common.validation import validate_steps, validate_weight

import pandas as pd
from tqdm import tqdm
tqdm.pandas()


def feedback(secret: str, guess: str) -> str:
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
    str
        A str object representing the status of each letter in the guess. The str is 5 characters long, each corresponding to one letter in the guess.
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

    return "".join(answer)


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
    # Create a copy of the words DataFrame to work with, avoiding modifications to the original DataFrame.
    words_aux: pd.DataFrame = words.copy()
    words_count: int = len(words_aux)

    # Apply the feedback function to each word in the DataFrame to generate an "answer code".
    words_aux["answer"] = words_aux.word.apply(
        lambda x: feedback(word, x)
    )

    # Calculate the frequency of each unique "answer code" in the DataFrame.
    answer_frequencies = words_aux.answer.value_counts()
    # Convert the frequencies to probabilities by dividing each frequency by the total number of words.
    answer_probabilities = answer_frequencies / words_count

    # For each probability, compute `prob * log2(prob)` and accumulate the results. The sum is negated to match the definition of entropy.
    entropy_sum = -reduce(
        lambda acc, prob: acc + prob * log2(prob),
        answer_probabilities,
        0
    )

    return entropy_sum

def process_entropies_chunk(chunk: pd.DataFrame, possible_words: pd.DataFrame) -> pd.DataFrame:
    """
    Calculates the entropy for each word in a DataFrame chunk.

    This function applies the entropy calculation to each word in a given chunk of the DataFrame, using the possible words provided. The entropy values are stored in a new column called "entropy".

    Parameters
    ----------
    chunk : pd.DataFrame
        A chunk of the DataFrame containing a subset of words to process.
    possible_words : pd.DataFrame
        The DataFrame containing the set of possible words used for entropy calculation.

    Returns
    -------
    pd.DataFrame
        The input chunk with an additional column, "entropy", containing the calculated entropy for each word.
    """

    chunk["entropy"] = chunk.word.apply(
        lambda word: entropy(word, possible_words)
    )
    return chunk




def get_entropies(steps: list[dict[str, str]], language: Language, parallelize: bool = True) -> pd.DataFrame:
    """
    Get the entropy for each word in a list of possible words based on a series of steps (guesses and their outcomes).

    Parameters:
    -----------
    steps : list[dict[str, str]]
        A list of dictionaries where each dictionary represents a guess and its corresponding outcome (answer). Each dictionary in the list should have the following structure:
        {
            "guess": "word_guessed",
            "answer": "feedback_code"
        }
        The "guess" is the word guessed, and "answer" is the feedback received (a string representing the status of each letter).
        
    language : Language
        A Language object for which the word list and cache files are to be loaded. This language's code is used to access the correct files within the `data/{language.code}/` directory.

    parallelize : bool, optional
        If `True`, the entropy calculations are parallelized across multiple processes to improve performance. Defaults to `True`.

    Returns:
    --------
    pd.DataFrame
        A DataFrame with the entropy values for each word. If the entropy values for the current steps have already been calculated and cached, they are loaded from the cache. Otherwise, the entropies are calculated and stored in the cache for future use. The resulting DataFrame contains all words along with their calculated entropy values.

    Raises:
    -------
    InvalidWordLengthError
        If a guess is not exactly 5 letters long.
    WordNotFoundError
        If a guess does not exist in the word list.
    InvalidAnswerError
        If an answer string is not valid.
    
    Process:
    --------
    1. Validates the input steps and language.
    
    2. Loads the list of all possible words from `data/{language.code}/words.csv`.
    
    3. Generates a cache path based on the series of steps. The cache directory structure is built using the guesses and their corresponding answers.
    
    4. Checks if the entropy values for the provided steps have been previously calculated and stored in the cache:
        - If cached, loads the entropy values from the corresponding file.
        - If not cached, calculates the entropies by:
            a. Filtering the possible words based on the current steps.
            b. Applying the `entropy` function to each word in the full word list, either sequentially or in parallel.
            c. Saves the calculated entropies in the cache for future reference.
    
    5. Returns a DataFrame with the words and their entropy values.
    """

    # Validate input steps
    validate_steps(steps, language)

    # Load all words from the CSV file
    all_words: pd.DataFrame = pd.read_csv(f"data/{language.code}/words.csv")

    # Generate a cache path based on the sequence of steps
    cache_path = f"data/{language.code}/cache/" \
        + "".join(
            map(
                lambda x: f"guess={x['guess']}/answer={x['answer']}/",
                steps
            )
        )
    is_cached = os.path.exists(cache_path + "stats.csv")

    # If the entropy values are cached, load them
    if is_cached:
        cache = pd.read_csv(cache_path + "stats.csv")
        stats = pd.merge(all_words, cache, on="id")

    # If not cached, calculate the entropy values
    else:
        possible_words: pd.DataFrame = query.filter_words_accumulative(steps, language)
        words_aux: pd.DataFrame = all_words.copy()

        # Parallelize processes to reduce time
        if parallelize:
            n_processes = mp.cpu_count()
            chunks = split_chunks(words_aux, n_processes)

            # Map across n processes the calculation of entropies for a given chunk
            with mp.Pool(processes=n_processes) as pool:
                stats_chunks = pool.starmap(
                    process_entropies_chunk,
                    [(chunk, possible_words) for chunk in chunks]
                )

            # Rebuild full dataframe from dataframe chunks
            stats: pd.DataFrame = pd.concat(stats_chunks)

        else:
            # Apply the entropy function to calculate entropy for each word
            words_aux["entropy"] = words_aux.word.progress_apply(
                lambda word: entropy(word, possible_words)
            )

            stats: pd.DataFrame = words_aux

        # Create the cache directory if it doesn't exist
        if not os.path.exists(cache_path):
            os.makedirs(cache_path)

        # Save the calculated entropy values to the cache
        stats[["id", "entropy"]] \
            .to_csv(cache_path + "stats.csv", index=False)

    return stats


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

    # Validate input
    validate_weight(weight)

    # Create a copy of the words DataFrame to work with, avoiding modifications to the original DataFrame.
    words_aux: pd.DataFrame = words.copy()

    # Ensure the weight is a number between 0 and 1
    if weight < 0 or weight > 1:
        raise ValueError("The weight must be between 0 and 1.")

    # Calculate the 'guessability' score as a weighted average of entropy and probability
    words_aux["guessability"] = weight * words_aux.entropy + (1 - weight) * words_aux.probability

    # Find the word with the highest 'guessability' score
    guess: str = words_aux \
        .sort_values("guessability", ascending=False) \
        .reset_index() \
        .loc[0, "word"]

    return guess

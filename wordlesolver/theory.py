from math import log2
from functools import reduce
import os
import multiprocessing as mp

from wordlesolver.filter import filter_words_accumulative
from wordlesolver.common import feedback, split_chunks
from wordlesolver.core.common import validate_steps
from wordlesolver.core.variables import Language

import pandas as pd
from tqdm import tqdm
tqdm.pandas()


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


def get_entropies(
        steps: list[dict[str, str]],
        language: Language,
        parallelize: bool = True,
        recalculate: bool = False
    ) -> pd.DataFrame:
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

    if recalculate:
        if os.path.exists(cache_path + "stats.csv"):
            os.remove(cache_path + "stats.csv")

    is_cached = os.path.exists(cache_path + "stats.csv")

    # If the entropy values are cached, load them
    if is_cached:
        cache = pd.read_csv(cache_path + "stats.csv")
        stats = pd.merge(all_words, cache, on="id")

    # If not cached, calculate the entropy values
    else:
        possible_words: pd.DataFrame = filter_words_accumulative(steps, language)
        words_aux: pd.DataFrame = all_words.copy()

        # Parallelize processes to reduce time
        if parallelize:
            n_processes = mp.cpu_count() // 2
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


def best_guess(
        steps: list[dict[str, str]],
        language: Language
    ) -> str:
    """
    Determines the best word to guess based on a weighted average of entropy and probability.

    The function calculates a new column called 'guessability' for each word, which is a weighted average of the entropy and probability columns. The word with the highest guessability score is then selected as the best guess.

    Parameters:
    ----------
    steps : list[dict[str, str]]
        A list of dictionaries where each dictionary represents a guess and its corresponding outcome (answer). Each dictionary in the list should have the following structure:
        {
            "guess": "word_guessed",
            "answer": "feedback_code"
        }
        The "guess" is the word guessed, and "answer" is the feedback received (a string representing the status of each letter).
        
    language : Language
        A Language object for which the word list and cache files are to be loaded. This language's code is used to access the correct files within the `data/{language.code}/` directory.

    Returns:
    -------
    str
        The word with the highest guessability score, which is considered the best guess.

    Raises:
    ------
    ValueError
        If the weight is not between 0 and 1, a ValueError is raised.
    """

    stats: pd.DataFrame = get_entropies(steps, language)
    possible_words: pd.DataFrame = filter_words_accumulative(steps, language)

    n_words_left: int = len(possible_words)

    # Normalize (min-max normalization) entropy to make it an even average
    stats["entropy_norm"] = (
        (stats.entropy - stats.entropy.min()) 
        / (stats.entropy.max() - stats.entropy.min())
    )

    possible_words["is_possible"] = 1
    possible_words = possible_words[["id", "is_possible"]]

    # Extend statistics with column indicating whether a word is still possible or not
    stats_ext: pd.DataFrame = pd.merge(stats, possible_words, on="id", how="left")
    stats_ext.is_possible = stats_ext.is_possible.fillna(0)

    max_weight = 0.8
    min_weight = 0.2

    # Calculate the ratio of possible words to the total number of words
    ratio = n_words_left / language.threshold

    # Calculate entropy based on possible words left
    entropy_weight = min_weight + (max_weight - min_weight) * ratio

    # Calculate the 'guessability' score as a weighted average of entropy and normalized probability while also taking into account whether a word is possible after filtering
    stats_ext["guessability"] = stats_ext.apply(
        lambda row:
            (
                entropy_weight * row.entropy_norm
                + (1 - entropy_weight) * row.probability
            )
            + row.is_possible / n_words_left
        , axis=1
    )

    # Find the word with the highest 'guessability' score
    guess: str = stats_ext \
        .sort_values("guessability", ascending=False) \
        .reset_index() \
        .loc[0, "word"]

    return guess

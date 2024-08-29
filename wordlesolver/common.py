import pandas as pd

from wordlesolver.core.variables import Status


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


def split_chunks(df: pd.DataFrame, n_chunks: int) -> list[pd.DataFrame]:
    """
    Splits a DataFrame into a specified number of chunks.

    This function divides a DataFrame into a list of smaller DataFrames, distributing rows as evenly as possible across the chunks. If the number of rows does not divide evenly, the remainder is distributed across the first few chunks.

    Parameters
    ----------
    df : pd.DataFrame
        The DataFrame to be split into chunks.
    n_chunks : int
        The number of chunks to split the DataFrame into.

    Returns
    -------
    list[pd.DataFrame]
        A list containing the resulting DataFrame chunks.

    Notes
    -----
    - The first few chunks may have one more row than the others if the row count isn't divisible by `n_chunks`.
    - The function handles edge cases where the number of chunks is greater than the number of rows by returning as many chunks as possible with one row each and empty DataFrames for the rest.
    """

    chunks: list[pd.DataFrame] = []
    accumulate_rows: int = 0

    row_count: int = len(df)
    base_chunk_size: int = row_count // n_chunks
    remaining_rows: int = row_count % n_chunks

    for i in range(n_chunks):
        extra_row = i < remaining_rows
        chunk_size = base_chunk_size + extra_row

        chunk = df.iloc[accumulate_rows : accumulate_rows + chunk_size]
        chunks.append(chunk)

        accumulate_rows += chunk_size

    return chunks

import pandas as pd


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

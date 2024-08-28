import pandas as pd


def split_chunks(df: pd.DataFrame, n_chunks: int) -> list[pd.DataFrame]:
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

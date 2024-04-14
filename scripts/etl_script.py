import numpy as np
import pandas as pd
import re


def read_csv(path: str, sep: str, zfill_cols: list) -> pd.DataFrame:
    """
    read csv data based on a given path and standardizes CNPJ columns
    """

    df = pd.read_csv(path,
                         sep=sep)

    for col in zfill_cols:
        if col in df.columns:
            max_len = df[col].astype(str).map(len).max()
            df[col] = df[col].astype(str).str.zfill(max_len)
        else:
            print(f"Warning: there is no '{col}' column.")

    return df

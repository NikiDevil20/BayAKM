import os

import pandas as pd

from src.bayakm.dir_paths import DirPaths

dirs = DirPaths()

def check_output(path: str = dirs.output_path) -> bool:
    return os.path.exists(path)

def create_output(df: pd.DataFrame) -> None:
    df.to_csv(
        dirs.output_path,
        sep=";",
        decimal=",",
        header=True,
        mode="w",
        index=False
    )

def append_to_output(df: pd.DataFrame) -> None:
    df.to_csv(
        dirs.output_path,
        sep=";",
        decimal=",",
        header=False,
        mode="a",
        index=False
    )

def import_output_to_df(path: str = dirs.output_path) -> pd.DataFrame:
    df = pd.read_csv(filepath_or_buffer=path, sep=";", decimal=",")
    return df.drop("Journal number", axis=1)

def split_import_df(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    measurements = df[df["Yield"].notna()]
    pending = df[df["Yield"].isna()]
    return measurements, pending

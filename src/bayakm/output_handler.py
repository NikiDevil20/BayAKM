import os

import pandas as pd

from src.bayakm.dir_paths import DirPaths


def check_output() -> bool:
    dirs = DirPaths()
    return os.path.exists(dirs.output_path)

def create_output(df: pd.DataFrame) -> None:
    dirs = DirPaths()
    df.to_csv(
        dirs.output_path,
        sep=";",
        decimal=",",
        header=True,
        mode="w",
        index=False
    )

def read_from_output() -> pd.DataFrame:
    dirs = DirPaths()
    return pd.read_csv(
        dirs.output_path,
        sep=";",
        decimal=","
    )

def append_to_output(df: pd.DataFrame) -> None:
    dirs = DirPaths()
    df.to_csv(
        dirs.output_path,
        sep=";",
        decimal=",",
        header=False,
        mode="a",
        index=False
    )

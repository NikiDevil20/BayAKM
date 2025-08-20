"""Contains functions for handling the recommendation
and measurements.
"""
import os
from time import time

import pandas as pd

from src.bayakm.config_loader import Config
from src.bayakm.dir_paths import DirPaths

dirs = DirPaths()
cfg = Config()


def check_path(path: str) -> bool:
    """Checks, if a path exists.
    Args:
        path: The path to check.
    Returns:
        bool: bool, if the path exists.
    """
    return os.path.exists(path)


def create_output(df: pd.DataFrame) -> None:
    """Takes a pd.DataFrame and writes it to the dirs.output_path.
    Args:
        df: The pd.DataFrame
    Returns:
        None
    """
    df.to_csv(
        dirs.output_path,
        sep=";",
        decimal=".",
        header=True,
        mode="w",
        index=False
    )


def append_to_output(df: pd.DataFrame) -> None:
    """Takes a pd.DataFrame and appends it to the dirs.output_path.
        Args:
            df: The pd.DataFrame
        Returns:
            None
        """
    df.to_csv(
        dirs.output_path,
        sep=";",
        decimal=".",
        header=False,
        mode="a",
        index=False
    )


def import_output_to_df() -> pd.DataFrame:
    """Reads the results.csv file, saves it in a pd.DataFrame and
    drops the "Journal number" column.
    Returns:
        pd.DataFrame: The pd.DataFrame that was read from the results.csv,
        without the "Journal number" column.
    """
    info_string("Measurements", "Reading results.csv...")
    df = pd.read_csv(
        filepath_or_buffer=dirs.output_path,
        sep=";",
        decimal="."
    )
    return df


def split_import_df(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Takes a pd.DataFrame which was read from the results file and splits it up
    in measurements (those contain measured yields) and pending experiments without
    measured yields.
    The returned pd.DataFrames might be empty.
    Args:
        df: The pd.DataFrame.
    Returns:
        The two pd.DataFrames containing only rows with
        measurements and without (pending).
    """
    measurements = df[df["Yield"].notna()]
    pending = df[df["Yield"].isna()]
    return measurements, pending


def welcome_string() -> float:
    line = 80 * "="
    welcome_msg = "BayAKM - script for chemical reaction optimization".center(80)
    print(line)
    print(welcome_msg)
    print(line)

    info_string("Settings", f"PI: {cfg.pi}")
    info_string("Settings", f"PI threshold: {cfg.pi_threshold}")
    info_string("Settings", f"Journal Prefix: {cfg.prefix}")
    print(line)
    return time()


def finished_string(start_time) -> None:
    line = 80 * "="
    total_time = time()-start_time
    success_string = f"New recommendation successfully appended to results!"
    timer = f"Total time: {total_time:.2f} s."
    final_string = f"Time to run some experiments :)"

    print(line)
    print(success_string)
    print(timer)
    print(line)
    print(final_string)
    print(line)


def info_string(chapter: str, text: str):
    chapter_in_brackets: str = "[" + chapter + "]"

    while len(chapter_in_brackets) <= len("[Recommendation]"):  # type: ignore
        chapter_in_brackets += " "

    print(chapter_in_brackets + text)

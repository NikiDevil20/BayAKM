import pandas as pd
from src.bayakm.dir_paths import DirPaths

dirs = DirPaths()

def import_output_to_df(path: str = dirs.output_path) -> pd.DataFrame:
    df = pd.read_csv(filepath_or_buffer=path, sep=";", decimal=",")
    return df.drop(df["Journal Prefix"], axis=1)

def split_import_df(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    measurements = df[df["Yield"].notna()]
    pending = df[df["Yield"].isna()]
    return measurements, pending

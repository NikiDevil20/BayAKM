import os
import pandas as pd
from src.bayakm.dir_paths import DirPaths
from src.bayakm.import_handler import import_output_to_df, split_import_df

dirs = DirPaths()


if os.path.exists(dirs.output_path):
    full_input: pd.DataFrame = import_output_to_df(dirs.output_path)
    measurements, pending = split_import_df(full_input)

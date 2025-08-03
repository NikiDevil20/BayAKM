import os

import pandas as pd
from baybe.campaign import Campaign

from src.bayakm.campaign import load_campaign, create_campaign
from src.bayakm.dir_paths import DirPaths
from src.bayakm.import_handler import import_output_to_df, split_import_df

dirs = DirPaths()

def optimization_loop() -> None:
    if os.path.exists(dirs.output_path):
        full_input: pd.DataFrame = import_output_to_df(dirs.output_path)
        measurements, pending = split_import_df(full_input)

    if not os.path.exists(dirs.campaign_path):
        campaign: Campaign = create_campaign()
    else:
        campaign: Campaign = load_campaign(dirs.campaign_path)

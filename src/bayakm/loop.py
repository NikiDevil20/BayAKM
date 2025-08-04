import os

import numpy as np
import pandas as pd
from baybe.campaign import Campaign

from src.bayakm.campaign import load_campaign, create_campaign, attach_hook, save_campaign
from src.bayakm.dir_paths import DirPaths
from src.bayakm.config_handler import Config
from src.bayakm.pi_handler import print_pi
from src.bayakm.output_handler import (
    check_output, create_output, append_to_output,
    import_output_to_df, split_import_df)

dirs = DirPaths()
cfg = Config()

def optimization_loop() -> None:
    if not check_output(dirs.campaign_path):
        create_campaign()

    campaign: Campaign = load_campaign(dirs.campaign_path)

    if cfg.pi:
        campaign = attach_hook(campaign, [print_pi])

    if os.path.exists(dirs.output_path):
        full_input: pd.DataFrame = import_output_to_df(dirs.output_path)
        measurements, pending = split_import_df(full_input)
        if not measurements.empty:
            campaign.add_measurements(measurements)
        if pending.empty:
            pending = None
    else:
        pending = None

    recommendation = campaign.recommend(
        batch_size=1,
        pending_experiments=pending
    )
    recommendation["Journal number"] = cfg.prefix
    recommendation["Yield"] = np.nan
    if check_output(dirs.output_path):
        append_to_output(recommendation)
    else:
        create_output(recommendation)
    save_campaign(campaign, dirs.campaign_path)

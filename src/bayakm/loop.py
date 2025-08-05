import os

import numpy as np
import pandas as pd
from baybe.campaign import Campaign

from src.bayakm.full_campaign import FullCampaign, load_campaign, create_campaign
from src.bayakm.dir_paths import DirPaths
from src.bayakm.config_loader import Config
from src.bayakm.probability_of_improvement import print_pi
from src.bayakm.output import (
    check_path, create_output, append_to_output,
    import_output_to_df, split_import_df)

dirs = DirPaths()
cfg = Config()

def optimization_loop() -> None:
    if not check_path(dirs.campaign_path):
        create_campaign()

    cmp = FullCampaign()

    if cfg.pi:
        cmp.attach_hook([print_pi])

    if check_path(dirs.output_path):
        full_input: pd.DataFrame = import_output_to_df(dirs.output_path)
        measurements, pending = split_import_df(full_input)
        if not measurements.empty:
            cmp.campaign.add_measurements(measurements)
        if pending.empty:
            pending = None
    else:
        pending = None

    recommendation = cmp.campaign.recommend(
        batch_size=1,
        pending_experiments=pending
    )
    recommendation["Journal number"] = cfg.prefix
    recommendation["Yield"] = np.nan
    if check_path(dirs.output_path):
        append_to_output(recommendation)
    else:
        create_output(recommendation)
    cmp.save_campaign(dirs.campaign_path)

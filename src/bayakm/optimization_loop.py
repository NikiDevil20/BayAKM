"""Contains the main function of the optimization loop."""
from time import time

import numpy as np
import pandas as pd

from src.bayakm.bayakm_campaign import BayAKMCampaign
from src.bayakm.config_loader import Config
from src.environment_variables.dir_paths import DirPaths
from src.bayakm.output import (
    check_path, create_output, append_to_output,
    import_output_to_df, split_import_df, welcome_string,
    finished_string, info_string)
from src.bayakm.probability_of_improvement import print_pi

dirs = DirPaths()
cfg = Config()
time_list = []


def optimization_loop() -> None:
    """Main function of the module. Performs the
    optimization loop.
    """

    start_time = welcome_string()

    bayakm = BayAKMCampaign()
    if cfg.pi:
        bayakm.attach_hook([print_pi])

    info_string("Measurements", "Checking for results.csv...")
    if check_path(dirs.output_path):
        full_input: pd.DataFrame = import_output_to_df()
        measurements, pending = split_import_df(full_input)

        if not measurements.empty:
            info_string("Measurements", "Adding measurements...")
            bayakm.campaign.add_measurements(measurements)

            info_string("Measurements", "Measurements added to campaign.")
        if pending.empty:
            pending = None
    else:
        pending = None

    info_string("Recommendation", "Getting recommendation...")
    time_list.append(time())
    recommendation = bayakm.campaign.recommend(
        batch_size=1,
        pending_experiments=pending
    )
    time_list.append(time())

    recommendation["Journal number"] = cfg.prefix
    recommendation["Yield"] = np.nan

    info_string("Recommendation", f"Recommendation obtained in {time_list[1]-time_list[0]:.2f} s.")

    if check_path(dirs.output_path):
        append_to_output(recommendation)
    else:
        create_output(recommendation)

    bayakm.save_campaign()

    finished_string(start_time)

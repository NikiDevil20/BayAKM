"""Contains the main function of the optimization loop."""
from time import time

import numpy as np
import pandas as pd

from src.bayakm.bayakm_campaign import BayAKMCampaign
from src.bayakm.config_loader import Config
from src.bayakm.dir_paths import DirPaths
from src.bayakm.output import (
    check_path, create_output, append_to_output,
    import_output_to_df, split_import_df, welcome_string,
    finished_string)
from src.bayakm.probability_of_improvement import print_pi

dirs = DirPaths()
cfg = Config()
time_list = []

def optimization_loop() -> None:
    """Main function of the module. Performs the
    optimization loop.
    """
    welcome_string()
    time_list.append(time())
    print(" Initializing campaign...")
    bayakm = BayAKMCampaign()

    if cfg.pi:
        print(" Attaching 'print_pi'-hook...")
        bayakm.attach_hook([print_pi])

    print(" Looking for results.csv...")
    if check_path(dirs.output_path):
        print(" Reading results.csv...")
        full_input: pd.DataFrame = import_output_to_df()
        measurements, pending = split_import_df(full_input)
        if not measurements.empty:
            print(" Adding measurements to campaign...")
            bayakm.campaign.add_measurements(measurements)
            print(" Measurements added to campaign.")
        if pending.empty:
            pending = None
    else:
        print(" Results.csv not found.")
        pending = None

    print(" Getting recommendation...")

    time_list.append(time())

    recommendation = bayakm.campaign.recommend(
        batch_size=1,
        pending_experiments=pending
    )

    time_list.append(time())

    recommendation["Journal number"] = cfg.prefix
    recommendation["Yield"] = np.nan

    print(f" Recommendation obtained in {time_list[2]-time_list[1]:.2f} s.")

    if check_path(dirs.output_path):
        append_to_output(recommendation)
    else:
        create_output(recommendation)

    print(" Overwriting campaign savefile...")
    bayakm.save_campaign()

    time_list.append(time())

    finished_string(time_list)

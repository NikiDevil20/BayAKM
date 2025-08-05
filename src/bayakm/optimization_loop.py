"""Contains the main function of the optimization loop."""
import numpy as np
import pandas as pd
import sys

from src.bayakm.config_loader import Config
from src.bayakm.dir_paths import DirPaths
from src.bayakm.bayakm_campaign import BayAKMCampaign
from src.bayakm.output import (
    check_path, create_output, append_to_output,
    import_output_to_df, split_import_df)
from src.bayakm.probability_of_improvement import print_pi

dirs = DirPaths()
cfg = Config()

def optimization_loop() -> None:
    """Main function of the module. Performs the
    optimization loop.
    """

    bayakm = BayAKMCampaign()

    if cfg.pi:
        bayakm.attach_hook([print_pi])

    if check_path(dirs.output_path):
        print("results.csv found.")
        full_input: pd.DataFrame = import_output_to_df()
        measurements, pending = split_import_df(full_input)
        if not measurements.empty:
            print("Measurements detected.")
            bayakm.campaign.add_measurements(measurements)
            print("Measurements added.")
        if pending.empty:
            pending = None
    else:
        pending = None
    print("Getting recommendation.")
    recommendation = bayakm.campaign.recommend(
        batch_size=1,
        pending_experiments=pending
    )

    recommendation["Journal number"] = cfg.prefix
    recommendation["Yield"] = np.nan

    print("Writing recommendation to output.")

    if check_path(dirs.output_path):
        append_to_output(recommendation)
    else:
        create_output(recommendation)

    print("Overwriting campaign.yaml.")
    bayakm.save_campaign()

    print("Check your new recommendation in the results.csv!")

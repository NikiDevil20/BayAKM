import sys

import pandas as pd
from baybe.acquisition.acqfs import ProbabilityOfImprovement
from baybe.objectives.base import Objective
from baybe.recommenders import BotorchRecommender
from baybe.searchspace import SearchSpace

from src.bayakm.config_loader import Config
from src.bayakm.dir_paths import DirPaths
from src.bayakm.output import info_string

dirs = DirPaths()
cfg = Config()


def print_pi(
        self: BotorchRecommender,
        searchspace: SearchSpace,
        objective: Objective | None = None,
        measurements: pd.DataFrame | None = None
) -> None:
    """Prints the fraction of candidates with a probability of improvement
    above the threshold defined in the configuration.
    Args:
        self (BotorchRecommender): The BotorchRecommender object.
        searchspace (SearchSpace): The SearchSpace object containing the
            candidates.
        objective (Objective): The Objective object, if any.
        measurements (pd.DataFrame): The measurements DataFrame, if any.
    Returns:
        None
    Raises:
        TypeError: If the PI threshold is not a float.
    """
    try:
        pi_threshold = float(cfg.pi_threshold)
    except TypeError:
        print(f"Failed to convert entry {cfg.pi_threshold} to float.")
        sys.exit(1)

    candidates, _ = searchspace.discrete.get_candidates()
    acqf = ProbabilityOfImprovement()
    pi = self.acquisition_values(
        candidates,
        searchspace,
        objective,  # type: ignore
        measurements,  # type: ignore
        acquisition_function=acqf
    )

    n_pis_over = (pi > pi_threshold).sum()
    pi_fraction = n_pis_over / len(pi)

    info_string(
        "Recommendation",
        f"{pi_fraction:.0%} of candidates "
        f"have a PI > {pi_threshold:.0%}.")

import pandas as pd
import yaml
from baybe.acquisition.acqfs import ProbabilityOfImprovement
from baybe.objectives.base import Objective
from baybe.recommenders import BotorchRecommender
from baybe.searchspace import SearchSpace
from bayakm.src.dir_paths import DirPaths


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
        ValueError: If the PI threshold is not between 0 and 1.
    """
    dirs = DirPaths()
    try:
        with open(dirs.config_path, "r") as f:
            yaml_string = f.read()
    except FileNotFoundError:
        print(f"config.yaml not found at {dirs.config_path}.")

    config_dict = yaml.safe_load(yaml_string)
    try:
        pi_threshold = float(config_dict["pi_threshold"])
    except TypeError:
        print(f"Failed to convert entry {config_dict["pi_threshold"]} to float.")



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
    pi_string: str = (f"{pi_fraction:.0%} of candidates "
                      f"have a PI > {pi_threshold:.0%}.")
    print(pi_string)
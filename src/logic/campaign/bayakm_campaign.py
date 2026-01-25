from types import MethodType
from typing import Callable

import numpy as np
import pandas as pd
import yaml
from baybe import Campaign
from baybe.acquisition import qProbabilityOfImprovement
from baybe.objectives import SingleTargetObjective
from baybe.objectives.base import Objective
from baybe.parameters import SubstanceParameter, NumericalDiscreteParameter, NumericalContinuousParameter, \
    CategoricalParameter
from baybe.recommenders import TwoPhaseMetaRecommender, FPSRecommender, BotorchRecommender, RandomRecommender
from baybe.searchspace import SearchSpace
from baybe.surrogates import GaussianProcessSurrogate
from baybe.targets import NumericalTarget
from baybe.utils.basic import register_hooks


from src.logic.simulation.simulate_results import YieldSimulator
from src.logic.config.config_loader import Config
from src.environment.dir_paths import DirPaths
from src.logic.output.output import check_path, info_string, create_output, append_to_output
from src.logic.parameters.parameters import build_param_list, build_constraints, save_pi_to_file

dirs = DirPaths()


class BayAKMCampaign(Campaign):
    """An expansion of the baybe Class Campaign,
    that automatically handles creation of the
    campaign and adds further functionality.
    To change the campaign.yaml file location,
    change it inside the DirPaths Class.
    """

    def __init__(self, parameter_list=None, constraint_list=None):
        info_string("Campaign", "Initializing campaign...")

        self.cfg = Config()
        self.pi_list = []

        if check_path(dirs.environ):
            if not check_path(dirs.return_file_path("campaign")):
                if parameter_list is None:
                    parameter_list = build_param_list()
                if constraint_list is None:
                    constraint_list = build_constraints()
                self.campaign = create_campaign(parameter_list, constraint_list)
                self.save_campaign()
                self.hybrid = is_hybrid(parameter_list)
            else:
                self.campaign = load_campaign()

    def attach_hook(
            self,
            hook_list: list[Callable]
    ) -> None:
        """Attaches hooks to the BotorchRecommender's recommend method.
        Args:
            self: The BayAKMCampaign object.
            hook_list (list[Callable]): A list of hooks to be attached to the
                BotorchRecommender's recommend method.
        Returns:
            None
        """
        info_string("Campaign", "Attaching hook...")
        bayesian_recommender = BotorchRecommender(
            surrogate_model=GaussianProcessSurrogate(),
        )
        bayesian_recommender.recommend = MethodType(
            register_hooks(
                BotorchRecommender.recommend,
                post_hooks=hook_list,
            ),
            bayesian_recommender,
        )
        recommender = TwoPhaseMetaRecommender(
            initial_recommender=FPSRecommender(),
            recommender=bayesian_recommender,
        )
        self.campaign.recommender = recommender

    @staticmethod
    def print_pi(
        self,
        searchspace: SearchSpace,
        objective: Objective | None = None,
        measurements: pd.DataFrame | None = None,
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
        candidates, _ = searchspace.discrete.get_candidates()
        acqf = qProbabilityOfImprovement()
        pi = BotorchRecommender.acquisition_values(
            candidates,
            searchspace,
            objective,  # type: ignore
            measurements,  # type: ignore
            acquisition_function=acqf
        )

        n_pis_over = (pi > 0.01).sum()
        pi_fraction = n_pis_over / len(pi)
        pi_copy = pi

        save_pi_to_file(pi_fraction, pi_copy.to_numpy())

        info_string(
            "Recommendation",
            f"{pi_fraction:.0%} of candidates "
            f"have a PI > 0.01.")

    def save_campaign(self) -> None:
        """Method for saving the baybe Campaign to the campaign.yaml file.
        Args:
            self: The FullCampaign object.
        Returns:
            None
        """
        info_string("Campaign", "Overwriting campaign savefile...")
        campaign_dict = self.campaign.to_dict()
        with open(dirs.return_file_path("campaign"), "w") as f:
            yaml.dump(campaign_dict, f)

    def get_pi(self):
        candidates, _ = self.campaign.searchspace.discrete.get_candidates()
        acqf = qProbabilityOfImprovement()
        pi = self.campaign.acquisition_values(
            candidates,
            acqf,
        )
        n_pis_over = (pi > 0.01).sum()
        pi_fraction = n_pis_over / len(pi)
        save_pi_to_file(list(pi))

    def get_recommendation(
            self,
            initial: bool,
            full_input_with_yield=None,
            pending=None
    ):
        """

        :param initial: Boolean indicating if this is the initial recommendation.
        :param full_input_with_yield: DataFrame containing new measurements to be added to the campaign.
        :param pending: DataFrame containing pending experiments.
        """
        if isinstance(full_input_with_yield, pd.DataFrame):
            old_measurements = self.campaign.measurements

            number_parameters = len(self.campaign.parameters)
            if not old_measurements.empty:
                new_measurements = compare_input_df_with_measured(full_input_with_yield, old_measurements, number_parameters)
            else:
                new_measurements = full_input_with_yield
            if not new_measurements.empty:
                self.campaign.add_measurements(new_measurements)

        if isinstance(pending, pd.DataFrame):
            if pending.empty:
                pending = None

        if not initial:
            self.get_pi()

        recommendation = self.campaign.recommend(
            batch_size=int(self.cfg.dict["Batchsize"]),
            pending_experiments=pending
        )

        recommendation["Journal no."] = self.cfg.dict["Journal prefix"]

        recommendation["Batch"] = "1"
        if not self.campaign.measurements.empty and "Batch" in self.campaign.measurements.columns:
            batch_no_list = [int(v) for v in list(self.campaign.measurements["Batch"])]  # Type: ignore
            recommendation["Batch"] = max(batch_no_list) + 1

        if self.cfg.dict["Simulate results"]:
            recommendation = YieldSimulator().add_fake_results(recommendation)
        else:
            recommendation["Yield"] = np.nan
        if initial:
            create_output(recommendation)
        else:
            append_to_output(recommendation)

    def get_param_dict(self) -> dict[str, list]:
        """
        :return: A dictionary with keys "substance", "numerical", "continuous", and "categorical",
                 each containing a list of the corresponding parameter types from the campaign.
        """
        param_dict = {
            "substance": [],
            "numerical": [],
            "continuous": [],
            "categorical": []
        }
        for parameter in self.campaign.parameters:
            if isinstance(parameter, SubstanceParameter):
                param_dict["substance"].append(parameter)

            elif isinstance(parameter, NumericalDiscreteParameter):
                param_dict["numerical"].append(parameter)

            elif isinstance(parameter, NumericalContinuousParameter):
                param_dict["continuous"].append(parameter)

            elif isinstance(parameter, CategoricalParameter):
                param_dict["categorical"].append(parameter)

            else:
                raise TypeError(f"Unknown parameter type: {type(parameter)}")
        return param_dict

    def get_parameter_list(self):
        """
        :return: A list of all parameters in the campaign.
        """
        return self.campaign.parameters


def create_campaign(parameter_list, constraint_list) -> Campaign:
    """Create a new campaign based on the parameters from
    the parameters in the parameters.yaml file.
    Returns:
        campaign (Campaign): The campaign object.
    """
    cfg = Config()

    searchspace = SearchSpace.from_product(
        parameters=parameter_list,
        constraints=constraint_list
    )
    target = NumericalTarget.normalized_sigmoid(name="Yield", anchors=[(0, 0.1), (1, 0.9)])

    objective = SingleTargetObjective(
        target=target
    )

    initial_recommender = RandomRecommender()

    if not is_hybrid(parameter_list):
        initial_recommender = FPSRecommender()

    recommender = TwoPhaseMetaRecommender(
        initial_recommender=initial_recommender,
        recommender=BotorchRecommender(
            acquisition_function=cfg.dict["Acquisition function"],
            hybrid_sampler="FPS"  # Type: ignore
        ),
        switch_after=1,
        remain_switched=True
    )
    campaign = Campaign(
        searchspace=searchspace,
        objective=objective,
        recommender=recommender,
    )
    return campaign


def load_campaign() -> Campaign:
    """Loads the campaign from its path defined
    in the DirPaths class and returns it.
    Returns:
        campaign (Campaign): The campaign as it was saved in the campaign.yaml file.
    """
    if not check_path(dirs.environ):
        raise FileNotFoundError(f"Campaign save file not found at {dirs.return_file_path('campaign')}")
    try:
        with open(dirs.return_file_path("campaign"), "r") as f:
            yaml_string: str = f.read()
    except FileNotFoundError:
        print(f"No file found at {dirs.return_file_path('campaign')}")

    campaign_dict = yaml.safe_load(yaml_string)
    return Campaign.from_dict(campaign_dict)


def compare_input_df_with_measured(
        df: pd.DataFrame,
        other_df: pd.DataFrame,
        n: int
) -> pd.DataFrame:
    """
    :param df: A DataFrame
    :param other_df: Another DataFrame, which is used for filtering out rows in the first DataFrame
    :param n: Number of rows to compare.
    :return: The DataFrame containing only unique rows.
    """
    compare_cols = list(df.columns[:n]) + [df.columns[-1]]

    missing_cols = [col for col in compare_cols if col not in other_df.columns]
    if missing_cols:
        raise ValueError(f"Missing columns in other_df: {missing_cols}")
    other_tuples = set(tuple(row) for row in other_df[compare_cols].values)
    mask = df[compare_cols].apply(lambda row: tuple(row) not in other_tuples, axis=1)
    return df[mask]


def is_hybrid(parameter_list) -> bool:
    """
    Flag that indicates if searchspace is hybrid.
    :param parameter_list: List of all parameters.
    :return: Bool, stating if searchspace is hybrid.
    """
    for parameter in parameter_list:
        if isinstance(parameter, NumericalContinuousParameter):
            return True
    return False




from types import MethodType
from typing import Callable

import numpy as np
import pandas as pd
import yaml
from baybe import Campaign
from baybe.objectives import SingleTargetObjective
from baybe.parameters import SubstanceParameter, NumericalDiscreteParameter, NumericalContinuousParameter, \
    CategoricalParameter
from baybe.recommenders import TwoPhaseMetaRecommender, FPSRecommender, BotorchRecommender, RandomRecommender, \
    KMeansClusteringRecommender
from baybe.searchspace import SearchSpace
from baybe.surrogates import GaussianProcessSurrogate
from baybe.targets import NumericalTarget
from baybe.utils.basic import register_hooks
from baybe.utils.interval import Interval
from baybe.utils.dataframe import add_fake_measurements

from src.bayakm.simulalte_results import YieldSimulator
from src.bayakm.config_loader import Config
from src.environment_variables.dir_paths import DirPaths
from src.bayakm.output import check_path, info_string, create_output, append_to_output
from src.bayakm.parameters import build_param_list

dirs = DirPaths()


class BayAKMCampaign(Campaign):
    """An expansion of the baybe Class Campaign,
    that automatically handles creation of the
    campaign and adds further functionality.
    To change the campaign.yaml file location,
    change it inside the DirPaths Class.
    """

    def __init__(self, parameter_list=None):
        info_string("Campaign", "Initializing campaign...")

        self.cfg = Config()

        if check_path(dirs.environ):
            if not check_path(dirs.return_file_path("campaign")):
                if parameter_list is None:
                    parameter_list = build_param_list()
                self.campaign = create_campaign(parameter_list)
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

        recommendation = self.campaign.recommend(
            batch_size=int(self.cfg.dict["Batchsize"]),
            pending_experiments=pending
        )

        recommendation["Journal number"] = self.cfg.dict["Journal prefix"]

        recommendation["Batch no."] = "1"
        if not self.campaign.measurements.empty and "Batch no." in self.campaign.measurements.columns:
            batch_no_list = [int(v) for v in list(self.campaign.measurements["Batch no."])]  # Type: ignore
            recommendation["Batch no."] = max(batch_no_list) + 1

        if self.cfg.dict["Simulate results"]:
            # target = NumericalTarget(
            #     mode="MAX",  # type: ignore
            #     name="Yield",
            #     transformation=None,
            #     bounds=Interval(lower=0, upper=100)
            # )
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


def create_campaign(parameter_list) -> Campaign:
    """Create a new campaign based on the parameters from
    the parameters in the parameters.yaml file.
    Returns:
        campaign (Campaign): The campaign object.
    """
    cfg = Config()

    searchspace = SearchSpace.from_product(
        parameters=parameter_list,
        constraints=[]
    )
    target = NumericalTarget.normalized_sigmoid(name="Yield", anchors=[(0, 0.1), (1, 0.9)])

    objective = SingleTargetObjective(
        target=target
    )
    # recommender = TwoPhaseMetaRecommender(
    #     initial_recommender=FPSRecommender(),
    #     recommender=BotorchRecommender(
    #         acquisition_function=cfg.dict["Acquisition function"],
    #         hybrid_sampler="FPS",
    #     ),
    #     switch_after=1,
    #     remain_switched=True
    # )

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




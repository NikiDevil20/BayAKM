from types import MethodType
from typing import Callable

import numpy as np
import pandas as pd
import yaml
from baybe import Campaign
from baybe.objectives import SingleTargetObjective
from baybe.parameters import SubstanceParameter, NumericalDiscreteParameter, NumericalContinuousParameter
from baybe.recommenders import TwoPhaseMetaRecommender, FPSRecommender, BotorchRecommender
from baybe.searchspace import SearchSpace
from baybe.surrogates import GaussianProcessSurrogate
from baybe.targets import NumericalTarget
from baybe.utils.basic import register_hooks
from baybe.utils.interval import Interval
from baybe.utils.dataframe import add_fake_measurements

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
                self.campaign = create_campaign(parameter_list)
                self.save_campaign()
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
            measurements=None,
            pending=None
    ):
        if isinstance(measurements, pd.DataFrame):
            self.campaign.add_measurements(measurements)

        if isinstance(pending, pd.DataFrame):
            if pending.empty:
                pending = None

        recommendation = self.campaign.recommend(
            batch_size=int(self.cfg.dict["Batchsize"]),
            pending_experiments=pending
        )

        recommendation["Journal number"] = self.cfg.dict["Journal prefix"]
        if self.cfg.dict["Simulate results"]:
            target = NumericalTarget(
                mode="MAX",  # type: ignore
                name="Yield",
                transformation=None,
                bounds=Interval(lower=0, upper=100)
            )
            recommendation = add_fake_measurements(recommendation, targets=[target])
        else:
            recommendation["Yield"] = np.nan

        if initial:
            create_output(recommendation)
        else:
            append_to_output(recommendation)


def create_campaign(parameter_list=None) -> Campaign:
    """Create a new campaign based on the parameters from
    the parameters in the parameters.yaml file.
    Returns:
        campaign (Campaign): The campaign object.
    """
    cfg = Config()
    if parameter_list is None:
        parameter_list: list[SubstanceParameter | NumericalDiscreteParameter | NumericalContinuousParameter] = build_param_list()

    searchspace = SearchSpace.from_product(
        parameters=parameter_list,
        constraints=[]
    )

    objective = SingleTargetObjective(
        target=NumericalTarget(
            mode="MAX",  # type: ignore
            name="Yield",
            transformation=None,
            bounds=Interval(lower=0, upper=100)
        )
    )
    # recommender = TwoPhaseMetaRecommender(
    #     initial_recommender=FPSRecommender(),
    #     recommender=BotorchRecommender(
    #         acquisition_function=cfg.dict["Acquisition function"],
    #         hybrid_sampler="FPS",  # Zufällige Auswahl der diskreten Kombinationen
    #     ),
    #     switch_after=1,
    #     remain_switched=True
    # )
    recommender = TwoPhaseMetaRecommender(
        recommender=BotorchRecommender(
            acquisition_function=cfg.dict["Acquisition function"],
            hybrid_sampler="FPS"
        ),
    )
    campaign = Campaign(
        searchspace=searchspace,
        objective=objective,
        recommender=recommender
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

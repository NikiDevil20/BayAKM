from types import MethodType
from typing import Callable

import yaml
from baybe import Campaign
from baybe.objectives import SingleTargetObjective
from baybe.parameters import SubstanceParameter, NumericalDiscreteParameter
from baybe.recommenders import TwoPhaseMetaRecommender, FPSRecommender, BotorchRecommender
from baybe.searchspace import SearchSpace
from baybe.surrogates import GaussianProcessSurrogate
from baybe.targets import NumericalTarget
from baybe.utils.basic import register_hooks

from src.bayakm.dir_paths import DirPaths
from src.bayakm.param_handler import build_param_list
from src.bayakm.config_handler import Config
from src.bayakm.pi_handler import print_pi
from src.bayakm.output_handler import check_path

dirs = DirPaths()

class FullCampaign(Campaign):
    def __init__(self):

        if not check_path(dirs.campaign_path):
            self.campaign = create_campaign()
            self.save_campaign(dirs.campaign_path)
        else:
            self.campaign = load_campaign(dirs.campaign_path)

    def attach_hook(
            self,
            hook_list: list[Callable]
    ) -> None:
        """Attaches hooks to the BotorchRecommender's recommend method.
        Args:
            hook_list (list[Callable]): A list of hooks to be attached to the
                BotorchRecommender's recommend method.
        Returns:
            campaign (Campaign): The Campaign class object with the attached hooks.
        """
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

    def save_campaign(self, file: str = dirs.campaign_path) -> None:
        campaign_dict = self.campaign.to_dict()
        with open(file, "w") as f:
            yaml.dump(campaign_dict, f)

def create_campaign() -> Campaign:
    param_list: list[SubstanceParameter | NumericalDiscreteParameter] = build_param_list()
    searchspace = SearchSpace.from_product(
        parameters=param_list,
        constraints=[]
    )
    objective = SingleTargetObjective(
        target=NumericalTarget(
            mode="MAX",  # type: ignore
            name="Yield",
            transformation=None
        )
    )
    recommender = TwoPhaseMetaRecommender(
        initial_recommender=FPSRecommender(),
        recommender=BotorchRecommender(
            acquisition_function="qLogEI"  # type: ignore
        ),
        switch_after=1,
        remain_switched=True
    )
    campaign = Campaign(
        searchspace=searchspace,
        objective=objective,
        recommender=recommender
    )
    return campaign

def load_campaign(file: str = dirs.param_path):
    with open(file, "r") as f:
        yaml_string: str = f.read()

    campaign_dict = yaml.safe_load(yaml_string)
    return Campaign.from_dict(campaign_dict)

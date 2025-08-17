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
from src.bayakm.output import check_path, info_string
from src.bayakm.parameters import build_param_list

dirs = DirPaths()


class BayAKMCampaign(Campaign):
    """An expansion of the baybe Class Campaign,
    that automatically handles creation of the
    campaign and adds further functionality.
    To change the campaign.yaml file location,
    change it insided the DirPaths Class.
    """

    def __init__(self, parameter_list=None):
        info_string("Campaign", "Initializing campaign...")
        if not check_path(dirs.campaign_path):
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
        with open(dirs.campaign_path, "w") as f:
            yaml.dump(campaign_dict, f)


def create_campaign(parameter_list=None) -> Campaign:
    """Create a new campaign based on the parameters from
    the parameters in the parameters.yaml file.
    Returns:
        campaign (Campaign): The campaign object.
    """
    if parameter_list is None:
        parameter_list: list[SubstanceParameter | NumericalDiscreteParameter] = build_param_list()
    searchspace = SearchSpace.from_product(
        parameters=parameter_list,
        constraints=[]
    )
    objective = SingleTargetObjective(
        target=NumericalTarget(
            mode="MAX",  # type: ignore
            name="Yield",
            transformation=None,
            bounds=[0, 100]
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


def load_campaign() -> Campaign:
    """Loads the campaign from its path defined
    in the DirPaths class and returns it.
    Returns:
        campaign (Campaign): The campaign as it was saved in the campaign.yaml file.
    """
    if not check_path(dirs.campaign_path):
        raise FileNotFoundError(f"Campaign save file not found at {dirs.campaign_path}")

    with open(dirs.campaign_path, "r") as f:
        yaml_string: str = f.read()

    campaign_dict = yaml.safe_load(yaml_string)
    return Campaign.from_dict(campaign_dict)

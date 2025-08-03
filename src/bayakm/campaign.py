from types import MethodType
from typing import Callable

from baybe import Campaign
from baybe.objectives import SingleTargetObjective
from baybe.parameters import SubstanceParameter, NumericalDiscreteParameter
from baybe.recommenders import TwoPhaseMetaRecommender, FPSRecommender, BotorchRecommender
from baybe.searchspace import SearchSpace
from baybe.surrogates import GaussianProcessSurrogate
from baybe.targets import NumericalTarget
from baybe.utils.basic import register_hooks

from src.bayakm.param_handler import build_param_list


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
            acquisition_function="qLogEi"  # type: ignore
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

def attach_hook(
        campaign: Campaign,
        hook_list: list[Callable]
) -> Campaign:
    """Attaches hooks to the BotorchRecommender's recommend method.
    Args:
        campaign (Campaign): The Campaign class object.
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
    campaign.recommender = recommender
    return campaign

# class CampaignPlus(Campaign):
#     def __init__(self):
#         Campaign.__init__(self)
#
#         self.pending: pd.DataFrame
#         self.recommendations: pd.DataFrame


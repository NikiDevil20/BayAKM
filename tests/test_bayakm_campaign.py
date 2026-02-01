import pytest
from baybe import Campaign
from baybe.objectives import SingleTargetObjective

from baybe.parameters.numerical import NumericalDiscreteParameter
from baybe.parameters.substance import SubstanceParameter
from baybe.recommenders import RandomRecommender, FPSRecommender, TwoPhaseMetaRecommender, BotorchRecommender
from baybe.searchspace import SearchSpace
from baybe.targets import NumericalTarget
from baybe.acquisition.acqfs import qLogExpectedImprovement

from src.logic.campaign.bayakm_campaign import create_campaign


class TestBayakmCampaign:
    def setup_method(self):
        self.num1 = NumericalDiscreteParameter(name="num1", values=(1, 2, 3))
        self.sub1 = SubstanceParameter(name="sub1", data={"water": "O", "ethanol": "CCO"})
        self.param_list = [self.num1, self.sub1]
        self.initial_recommender = FPSRecommender()
        self.target = NumericalTarget.normalized_sigmoid(name="Yield", anchors=[(0, 0.1), (1, 0.9)])
        self.objective = SingleTargetObjective(target=self.target)
        self. searchspace = SearchSpace.from_product(
            parameters=self.param_list,
        )
        self.acqf = qLogExpectedImprovement()
        self.recommender = TwoPhaseMetaRecommender(
            initial_recommender=self.initial_recommender,
            recommender=BotorchRecommender(
                acquisition_function=self.acqf,
                hybrid_sampler="FPS"
            ),
            switch_after=1,
            remain_switched=True
        )
        self.campaign = Campaign(
            searchspace=self.searchspace,
            objective=self.objective,
            recommender=self.recommender,
        )

    def test_create_campaign(self):
        assert create_campaign(parameter_list=self.param_list, acqf=self.acqf) == self.campaign


from baybe import Campaign
import pandas as pd
import os
from pathlib import Path

class CampaignPlus(Campaign):
    def __init__(self):
        Campaign.__init__(self)

        self.pending: pd.DataFrame
        self.recommendations: pd.DataFrame

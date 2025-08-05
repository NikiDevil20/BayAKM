"""Contains the DirPaths Class."""
import os
from pathlib import Path


class DirPaths:
    """Class for handling the paths inside the module."""
    def __init__(self):
        self.base_dir = Path(__file__).resolve().parents[2]

        self.bayakm_dir = os.path.join(self.base_dir, "src")

        self.src_dir = os.path.join(self.bayakm_dir, "bayakm")
        self.docs_dir = os.path.join(self.base_dir, "docs")
        self.tests_dir = os.path.join(self.base_dir, "tests")
        self.data_dir = os.path.join(self.bayakm_dir, "data")

        self.config_path = os.path.join(self.data_dir, "config.yaml")
        self.output_path = os.path.join(self.data_dir, "results.csv")
        self.param_path = os.path.join(self.data_dir, "parameters.yaml")
        self.campaign_path = os.path.join(self.data_dir, "campaign.yaml")

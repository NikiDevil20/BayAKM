"""Contains the DirPaths Class."""
import os
from pathlib import Path
from dataclasses import dataclass


@dataclass
class DirPaths:
    """Class for handling the paths inside the module."""
    base_dir = Path(__file__).resolve().parents[2]

    bayakm_dir = os.path.join(base_dir, "src")

    src_dir = os.path.join(bayakm_dir, "bayakm")
    docs_dir = os.path.join(base_dir, "docs")
    tests_dir = os.path.join(base_dir, "tests")
    data_dir = os.path.join(bayakm_dir, "data")

    config_path = os.path.join(data_dir, "config.yaml")
    output_path = os.path.join(data_dir, "results.csv")
    param_path = os.path.join(data_dir, "parameters.yaml")
    campaign_path = os.path.join(data_dir, "campaign.yaml")

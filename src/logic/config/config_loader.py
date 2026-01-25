"""Contains the Config Class."""
import os.path
import sys

import yaml

from src.environment.dir_paths import DirPaths

dirs = DirPaths()
config = dict[str, bool | float | str]


class Config:
    """Class for reading the settings chosen in the config.yaml file."""
    def __init__(self):
        if os.path.exists(dirs.environ):
            self.dict: config = self.load_from_yaml()
        else:
            self.dict = {
                "Campaign name": "My first Campaign",
                "Journal prefix": "",
                "Batchsize": 3,
                "Initial recommender": "FPS",
                "Acquisition function": "qLogEI",
                "Simulate results": False
            }

    def save_to_yaml(self, config_dict):
        if not os.path.exists(dirs.environ) or config_dict["Campaign name"] != self.load_from_yaml()["Campaign name"]:
            dirs.build_campaign_folder(
                config_dict["Campaign name"]
            )

        try:
            with open(dirs.return_file_path("config"), "w") as f:
                yaml.dump(config_dict, f)
        except FileNotFoundError:
            print(f"Could not locate config.yaml at {dirs.return_file_path('config')}")
            sys.exit(1)

    @staticmethod
    def load_from_yaml() -> config:
        try:
            with open(dirs.return_file_path("config"), "r") as f:
                yaml_string = f.read()
        except FileNotFoundError:
            print(f"Could not locate config.yaml at {dirs.return_file_path('config')}")
            sys.exit(1)
        return yaml.safe_load(yaml_string)

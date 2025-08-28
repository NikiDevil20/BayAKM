"""Contains the Config Class."""
import sys

import yaml

from src.bayakm.dir_paths import DirPaths

dirs = DirPaths()
config = dict[str, bool | float | str]


class Config:
    """Class for reading the settings chosen in the config.yaml file."""
    def __init__(self):
        self.dict: config = self.load_from_yaml()

        # self.pi: float = self.dict["PI_threshold"]
        # self.prefix: str = self.dict["Journal_prefix"]
        # self.initial_recommender: str = self.dict["Initial_recommender"]
        # self.acquisition_function: str = self.dict["Acquisition_function"]
        # self.batch_size: int = self.dict["Batch_size"]

    @staticmethod
    def save_to_yaml(config_dict):
        try:
            with open(dirs.config_path, "w") as f:
                yaml.dump(config_dict, f)
        except FileNotFoundError:
            print(f"Could not locate config.yaml at {dirs.config_path}")
            sys.exit(1)

    @staticmethod
    def load_from_yaml() -> config:
        try:
            with open(dirs.config_path, "r") as f:
                yaml_string = f.read()
        except FileNotFoundError:
            print(f"Could not locate config.yaml at {dirs.config_path}")
            sys.exit(1)
        return yaml.safe_load(yaml_string)

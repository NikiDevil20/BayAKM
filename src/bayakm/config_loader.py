"""Contains the Config Class."""
import yaml

from src.bayakm.dir_paths import DirPaths

dirs = DirPaths()

class Config:
    """Class for reading the settings chosen in the config.yaml file."""
    def __init__(self):
        try:
            with open(dirs.config_path, "r") as f:
                yaml_string: str = f.read()
        except:
            raise FileNotFoundError(f"Could not locate config.yaml at {dirs.config_path}")

        config_dict: dict[str, dict[str, bool | float | str]] = yaml.safe_load(yaml_string)
        content: dict[str, bool | float | str]= config_dict["config"]

        self.pi: bool = content["print_pi"]
        self.pi_threshold: float = content["pi_threshold"]
        self.prefix: str = content["journal_prefix"]
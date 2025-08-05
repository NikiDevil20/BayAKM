import yaml
from src.bayakm.dir_paths import DirPaths

dirs = DirPaths()

class Config:
    def __init__(self):
        try:
            with open(dirs.config_path, "r") as f:
                yaml_string: str = f.read()
        except FileNotFoundError:
            print(f"Could not locate config.yaml at {dirs.config_path}.")

        config_dict: dict[str, dict[str, bool | float | str]] = yaml.safe_load(yaml_string)
        content: dict[str, bool | float | str]= config_dict["config"]

        self.pi = content["print_pi"]
        self.pi_threshold = content["pi_threshold"]
        self.prefix = content["journal_prefix"]
import yaml
from ..src.bayakm.dir_paths import DirPaths
import os



class ParamHandler:
    def __init__(self):
        pt = DirPaths()
        self.param_input_path = os.path.join(pt.data_dir, "parameters.yaml")

    def read_params_from_yaml(self):
        with open(self.param_input_path, "r") as f:
            yaml_string = f.read()


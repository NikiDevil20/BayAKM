import os

import yaml
from baybe.parameters import SubstanceParameter

from bayakm.src.dir_paths import DirPaths

SMILES = str

def create_dict_from_yaml() -> dict[str, dict[str, dict[str, SMILES]]]:
    pt = DirPaths()
    param_path = os.path.join(pt.data_dir, "parameters.yaml")
    with open(param_path, "r") as f:
        yaml_string = f.read()
    return yaml.safe_load(yaml_string)


def build_substance_params() -> list[SubstanceParameter]:

    parameter_list: list[SubstanceParameter] = []
    yaml_string = create_dict_from_yaml()
    all_params_dict = yaml_string["Substance Parameters"]

    for key in all_params_dict.keys():
        parameter_list.append(
            SubstanceParameter(
                name=key,
                data=all_params_dict[key],
                decorrelate=0.7,
                encoding="MORDRED"  # type: ignore
            )
        )
    return parameter_list


class ParamHandler:
    def __init__(self):
        pt = DirPaths()
        self.param_input_path = os.path.join(pt.data_dir, "parameters.yaml")


def main():
    build_substance_params()

if __name__ == "__main__":
    main()
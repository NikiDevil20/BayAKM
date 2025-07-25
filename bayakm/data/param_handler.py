import os

import yaml
from baybe.parameters import SubstanceParameter, NumericalDiscreteParameter

from bayakm.src.dir_paths import DirPaths

SMILES = str

def create_dict_from_yaml() -> dict[str, dict[str, dict[str, SMILES] | tuple[float]]]:
    pt = DirPaths()
    param_path = os.path.join(pt.data_dir, "parameters.yaml")
    with open(param_path, "r") as f:
        yaml_string = f.read()
    return yaml.safe_load(yaml_string)


def build_substance_params() -> list[SubstanceParameter | NumericalDiscreteParameter]:

    parameter_list: list[SubstanceParameter | NumericalDiscreteParameter] = []
    yaml_string = create_dict_from_yaml()

    try:
        all_subst_dict = yaml_string["Substance Parameters"]
        for key in all_subst_dict.keys():
            parameter_list.append(
                SubstanceParameter(
                    name=key,
                    data=all_subst_dict[key],
                    decorrelate=0.7,
                    encoding="MORDRED"  # type: ignore
                )
            )
    except:
        print("No Substance Parameters detected. \n"
              "If you wanted to include Substance Parameters,"
              "check for spelling errors.")

    try:
        all_numeric_dict = yaml_string["Numerical Parameters"]
        for key in all_numeric_dict.keys():
            parameter_list.append(
                NumericalDiscreteParameter(
                    name=key,
                    values=all_numeric_dict[key]
                )
            )
    except:
        print("No Numerical Parameters detected. \n"
              "If you wanted to include Substance Parameters,"
              "check for spelling errors.")
    print(parameter_list)
    return parameter_list


class ParamHandler:
    def __init__(self):
        pt = DirPaths()
        self.param_input_path = os.path.join(pt.data_dir, "parameters.yaml")


def main():
    build_substance_params()

if __name__ == "__main__":
    main()
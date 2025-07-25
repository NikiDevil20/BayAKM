import os

import yaml
from baybe.parameters import SubstanceParameter, NumericalDiscreteParameter

from bayakm.src.dir_paths import DirPaths

SMILES = str


def build_param_list() -> list[SubstanceParameter | NumericalDiscreteParameter]:
    """Builds the parameters list from the parameters.yaml file.
    :return: A list of parameters.
    :raise: FileNotFoundError: If parameters.yaml is not found.
    """
    parameter_list: list[SubstanceParameter | NumericalDiscreteParameter] = []
    pt = DirPaths()
    param_path: str = os.path.join(pt.data_dir, "parameters.yaml")

    try:
        with open(param_path, "r") as f:
            yaml_string: str = f.read()
    except FileNotFoundError:
        print(f"Could not locate parameters.yaml at {param_path}.")

    yaml_dict: dict[str, dict[str, dict[str, SMILES] | tuple[float]]] \
        = yaml.safe_load(yaml_string)

    try:
        all_subst_dict: dict[str, dict[str, SMILES]] = yaml_dict["Substance Parameters"]
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
        all_numeric_dict: dict[str, tuple[float]] = yaml_dict["Numerical Parameters"]
        for key in all_numeric_dict.keys():
            parameter_list.append(
                NumericalDiscreteParameter(
                    name=key,
                    values=all_numeric_dict[key]
                )
            )
    except:
        print("No Numerical Parameters detected. \n"
              "If you wanted to include Numerical Parameters,"
              "check for spelling errors.")
    return parameter_list

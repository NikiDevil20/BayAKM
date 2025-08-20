import yaml
import sys
from time import time
from baybe.parameters import SubstanceParameter, NumericalDiscreteParameter

from src.bayakm.dir_paths import DirPaths

SMILES = str


def build_param_list() -> list[SubstanceParameter | NumericalDiscreteParameter | None]:
    """Builds the parameter list from the parameters.yaml file.
    Returns:
        A list of parameters.
    Raises:
        FileNotFoundError: If parameters.yaml is not found.
    """
    parameter_list: list[SubstanceParameter | NumericalDiscreteParameter] = []

    yaml_dict = load_yaml()

    if "Substance Parameters" in yaml_dict.keys():
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
    else:
        print("No Substance Parameters detected. \n"
              "If you wanted to include Substance Parameters,"
              "check for spelling errors.")

    if "Numerical Discrete Parameters" in yaml_dict.keys():
        all_numeric_dict: dict[str, tuple[float]] = yaml_dict["Numerical Discrete Parameters"]
        for key in all_numeric_dict.keys():
            parameter_list.append(
                NumericalDiscreteParameter(
                    name=key,
                    values=all_numeric_dict[key]
                )
            )
    else:
        print("No Numerical Parameters detected. \n"
              "If you wanted to include Numerical Parameters,"
              "check for spelling errors.")
    return parameter_list


def load_yaml() -> dict | None:
    dirs = DirPaths()
    try:
        with open(dirs.param_path, "r") as f:
            yaml_string: str = f.read()
    except FileNotFoundError:
        print(f"Could not locate parameters.yaml at {dirs.param_path}.")
        return {}

    return yaml.safe_load(yaml_string)


def save_yaml(yaml_dict: dict):
    dirs = DirPaths()
    with open(dirs.param_path, "w") as f:
        yaml.dump(yaml_dict, f)


def write_to_parameters_file(mode: str, parameter_name: str, parameter_values: list[float] | dict[str, SMILES]):
    yaml_dict = load_yaml()

    if mode == "numerical":
        if not "Numerical Discrete Parameters" in yaml_dict.keys():
            yaml_dict["Numerical Discrete Parameters"] = {parameter_name: parameter_values}
        else:
            yaml_dict["Numerical Discrete Parameters"][parameter_name] = parameter_values

    elif mode == "substance":
        if not "Substance Parameters" in yaml_dict.keys():
            yaml_dict["Substance Parameters"] = {parameter_name: parameter_values}
        else:
            yaml_dict["Substance Parameters"][parameter_name] = parameter_values
    save_yaml(yaml_dict)


def delete_parameter(parameter_names: list[str]):
    yaml_dict = load_yaml()

    for key in yaml_dict:
        yaml_dict[key] = {k: v for k, v in yaml_dict[key].items() if k not in parameter_names}

    save_yaml(yaml_dict)



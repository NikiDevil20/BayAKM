import os.path

import yaml
from baybe import Campaign
from baybe.parameters import SubstanceParameter, NumericalDiscreteParameter, NumericalContinuousParameter, \
    CategoricalParameter
from baybe.utils.interval import Interval

from src.environment_variables.dir_paths import DirPaths

SMILES = str


def build_param_list() -> list[SubstanceParameter | NumericalDiscreteParameter | NumericalContinuousParameter]:
    """Builds the parameter list from the parameters.yaml file.
    Returns:
        A list of parameters.
    Raises:
        FileNotFoundError: If parameters.yaml is not found.
    """
    parameter_list: list[SubstanceParameter | NumericalDiscreteParameter | NumericalContinuousParameter] = []

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
        print("No Substance Parameters detected.")

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
        print("No Numerical Discrete Parameters detected.")

    if "Numerical Continuous Parameters" in yaml_dict.keys():
        all_cont_dict: dict[str, tuple[float, float]] = yaml_dict["Numerical Continuous Parameters"]
        for key in all_cont_dict.keys():
            parameter_list.append(
                NumericalContinuousParameter(
                    name=key,
                    bounds=Interval(all_cont_dict[key][0], all_cont_dict[key][1])
                )
            )
    else:
        print("No Continuous Parameters detected.")

    return parameter_list


def load_yaml() -> dict | None:
    dirs = DirPaths()
    if os.path.exists(dirs.environ):

        try:
            with open(dirs.return_file_path("parameters"), "r") as f:
                yaml_string: str = f.read()
        except FileNotFoundError:
            print(f"Could not locate parameters.yaml at {dirs.return_file_path('parameters')}.")
            return {}

        return yaml.safe_load(yaml_string)
    else:
        print(f"Save the config file before creating parameters.")
        return {}


def save_yaml(yaml_dict: dict):
    dirs = DirPaths()
    if os.path.exists(dirs.environ):
        try:
            with open(dirs.return_file_path("parameters"), "w") as f:
                yaml.dump(yaml_dict, f)
        except FileNotFoundError:
            print(f"Parameter file not found at {dirs.return_file_path('parameters')}")


def write_to_parameters_file(
        mode: str, parameter_name: str,
        parameter_values: list[float] | dict[str, SMILES] | tuple[float, float]
):
    yaml_dict = load_yaml()

    if mode == "numerical":
        if "Numerical Discrete Parameters" not in yaml_dict.keys():
            yaml_dict["Numerical Discrete Parameters"] = {parameter_name: parameter_values}
        else:
            yaml_dict["Numerical Discrete Parameters"][parameter_name] = parameter_values

    elif mode == "substance":
        if "Substance Parameters" not in yaml_dict.keys():
            yaml_dict["Substance Parameters"] = {parameter_name: parameter_values}
        else:
            yaml_dict["Substance Parameters"][parameter_name] = parameter_values

    elif mode == "continuous":
        if "Numerical Continuous Parameters" not in yaml_dict.keys():
            yaml_dict["Numerical Continuous Parameters"] = {parameter_name: parameter_values}
        else:
            yaml_dict["Numerical Continuous Parameters"][parameter_name] = parameter_values

    save_yaml(yaml_dict)


def delete_parameter(parameter_names: list[str]):
    yaml_dict = load_yaml()

    for key in yaml_dict:
        yaml_dict[key] = {k: v for k, v in yaml_dict[key].items() if k not in parameter_names}

    save_yaml(yaml_dict)



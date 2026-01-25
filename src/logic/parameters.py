import os.path

import numpy as np
import yaml
from baybe import Campaign
from baybe.constraints import DiscreteExcludeConstraint, ThresholdCondition, SubSelectionCondition
from baybe.parameters import SubstanceParameter, NumericalDiscreteParameter, NumericalContinuousParameter, \
    CategoricalParameter
from baybe.utils.interval import Interval
from typing import Literal

from src.logic.output import info_string
from src.environment.dir_paths import DirPaths

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
        info_string("Parameters", "No Substance Parameters detected.")

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
        info_string("Parameters", "No Numerical Discrete Parameters detected.")

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
        info_string("Parameters", "No Numerical Continuous Parameters detected.")

    return parameter_list


def load_yaml() -> dict | None:
    """
    Reads the parameters.yaml file and returns its contents as a dictionary.
    If the file does not exist, it returns an empty dictionary.
    :return: A dictionary with all parameters.
    """
    dirs = DirPaths()
    if os.path.exists(dirs.environ):
        if os.path.exists(dirs.return_file_path("parameters")):
            with open(dirs.return_file_path("parameters"), "r") as f:
                yaml_string: str = f.read()
        # except FileNotFoundError:
        #     print(f"Could not locate parameters.yaml at {dirs.return_file_path('parameters')}.")
        #     return {}

            return yaml.safe_load(yaml_string)
        else:
            info_string("Parameters", "Parameter file not found.")
            info_string("Parameters", "If this is your first parameter, a new parameters.yaml file will be created.")
            return {}
    else:
        info_string("Parameters", "Save the config file before creating parameters.")
        return {}


def save_yaml(yaml_dict: dict):
    """
    Saves a given dictionary to the parameters.yaml file.
    If the file does not exist, it creates a new one.
    :param yaml_dict: A dictionary to be saved in the parameters.yaml file.
    """
    dirs = DirPaths()
    if os.path.exists(dirs.environ):
        with open(dirs.return_file_path("parameters"), "w") as f:
            yaml.dump(yaml_dict, f)
        # except FileNotFoundError:
        #     print(f"Parameter file not found at {dirs.return_file_path('parameters')}")


def write_to_parameters_file(
        mode: Literal["numerical", "substance", "continuous"],
        parameter_name: str,
        parameter_values: list[float] | dict[str, SMILES] | tuple[float, float]
) -> None | str:
    """
    Takes a new parameter's name and values and appends them to the parameters.yaml file.
    If the file does not exist, it creates a new one.
    :param mode:
    :param parameter_name:
    :param parameter_values:
    """
    yaml_dict = load_yaml()

    if check_name_exists(yaml_dict, parameter_name):
        return "Name already exists."

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
    return None


def write_constraints_to_file(first_condition, second_condition, combiner="AND"):
    yaml_dict = load_yaml()
    constraint_name = first_condition[0] + "_" + second_condition[0]
    constraint_dict = {
        "parameters": [first_condition[0], second_condition[0]],
        "conditions": [first_condition[1], second_condition[1]],
        "combiner": combiner
    }
    if "Constraints" not in yaml_dict.keys():
        yaml_dict["Constraints"] = {constraint_name: constraint_dict}
    else:
        yaml_dict["Constraints"][constraint_name] = constraint_dict

    save_yaml(yaml_dict)


def build_constraints() -> list:
    yaml_dict = load_yaml()
    constraint_list = []
    if "Constraints" in yaml_dict.keys():
        all_constraints_dict: dict[str, dict] = yaml_dict["Constraints"]
        for key in all_constraints_dict.keys():
            condition_list = []
            for condition in all_constraints_dict[key]["conditions"]:
                ctype = condition["type"]
                match ctype:
                    case "threshold":
                        condition = ThresholdCondition(
                            threshold=condition["threshold"],
                            operator=condition["operator"]
                        )
                    case "subselection":
                        condition = SubSelectionCondition(
                            selection=condition["selection"]
                        )

                condition_list.append(condition)

            constraint_list.append(
                DiscreteExcludeConstraint(
                    parameters=all_constraints_dict[key]["parameters"],
                    conditions=condition_list,
                    combiner=all_constraints_dict[key]["combiner"]
                )
            )
    else:
        info_string("Parameters", "No Constraints detected.")
    return constraint_list


def delete_parameter(parameter_names: list[str]):
    """
    Removes a parameter from the parameters.yaml file.
    :param parameter_names: A list of parameter names to be removed.
    """
    yaml_dict = load_yaml()

    for key in yaml_dict:
        yaml_dict[key] = {k: v for k, v in yaml_dict[key].items() if k not in parameter_names}

    save_yaml(yaml_dict)


def check_name_exists(
        parameter_dict: dict,
        parameter_name: str
) -> bool:
    """
    Checks if a parameter name already exists in a given dictionary.
    :param parameter_dict: A dictionary containing parameters.
    :param parameter_name: The name of the parameter to be checked.
    :return: True if the name exists, False otherwise.
    """
    for key in parameter_dict.keys():
        if isinstance(parameter_dict[key], dict) and parameter_name in parameter_dict[key]:
            return True
    return False


def save_pi_to_file(pi_fraction: float, pi_values: np.ndarray):
    """
    Saves the given PI fraction and values to the parameters.yaml file under the PI section.
    If the file does not exist, it creates a new one.
    :param pi_fraction: The fraction of candidates with PI above the threshold.
    :param pi_values: The array of PI values for all candidates.
    """
    yaml_dict = load_yaml()
    if "PI" not in yaml_dict.keys():
        yaml_dict["PI"] = []

    yaml_dict["PI"].append({
        "fraction": float(pi_fraction),
        "values": list(pi_values)
    })

    save_yaml(yaml_dict)


def load_pi_from_file() -> dict | None:
    """
    Reads the PI section from the parameters.yaml file and returns its contents as a dictionary.
    If the file does not exist, it returns None.
    :return: A dictionary with all PI data.
    """
    yaml_dict = load_yaml()
    if "PI" in yaml_dict.keys():
        return yaml_dict["PI"]
    else:
        info_string("Parameters", "No PI data found.")
        return None

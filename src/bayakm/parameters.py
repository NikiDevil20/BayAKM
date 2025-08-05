import yaml
from baybe.parameters import SubstanceParameter, NumericalDiscreteParameter

from src.bayakm.dir_paths import DirPaths

SMILES = str


def build_param_list() -> list[SubstanceParameter | NumericalDiscreteParameter]:
    """Builds the parameters list from the parameters.yaml file.
    Returns:
        A list of parameters.
    Raises:
        FileNotFoundError: If parameters.yaml is not found.
    """
    parameter_list: list[SubstanceParameter | NumericalDiscreteParameter] = []
    dirs = DirPaths()

    try:
        with open(dirs.param_path, "r") as f:
            yaml_string: str = f.read()
    except FileNotFoundError:
        print(f"Could not locate parameters.yaml at {dirs.param_path}.")

    yaml_dict: dict[str, dict[str, dict[str, SMILES] | tuple[float]]] \
        = yaml.safe_load(yaml_string)

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

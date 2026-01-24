import yaml
import os

from rdkit import Chem
from src.environment.dir_paths import DirPaths

SMILES = str
smiles_type = dict[str, dict[str, SMILES]]


dirs = DirPaths()


def smiles_dict_from_yaml() -> smiles_type:
    """
    Load a YAML file containing SMILES strings and return a dictionary.

    Returns:
        dict: A dict of molecule groups like solvents, bases etc.,
        which contains molecule names as keys and SMILES strings as values.
    """
    path = os.path.join(dirs.data, "smiles_strings.yaml")

    with open(path, 'r') as f:
        _smiles_dict: smiles_type = yaml.safe_load(f)
    return _smiles_dict


def verify_entries(_smiles_dict: smiles_type) -> None | str:
    """
    Verify that all entries in the SMILES dictionary are valid.

    Args:
        _smiles_dict (dict): A dict of molecule groups like solvents, bases etc.,
        which contains molecule names as keys and SMILES strings as values.
    Returns:
        error (str | None): Error message if any SMILES string is invalid, else None.
    """
    error = None

    for group, molecule in _smiles_dict.items():
        for name, smiles_string in molecule.items():

            if not is_valid_smiles(smiles_string):
                error = (
                    f"Invalid SMILES string for {name} in group {group}: {smiles_string}\n"
                    f"Common error include dots at the end or spaces "
                )

    return error


def is_valid_smiles(smiles: str) -> bool | str:
    """
    Verify that a single SMILES string is valid.

    Args:
        smiles (str): A SMILES string.
    Returns:
        bool | str: True if valid, error message if invalid.
    """
    mol = Chem.MolFromSmiles(smiles)

    return False if mol is None else True


def add_molecule_to_dict(
    name: str,
    smiles_string: str,
    group: str = "other"
) -> None | str:
    """
    Add a molecule to the SMILES dictionary.

    Args:
        which contains molecule names as keys and SMILES strings as values.
        group (str): The group to add the molecule to.
        name (str): The name of the molecule.
        smiles_string (str): The SMILES string of the molecule.
    Returns:
        error (str | None): Error message if SMILES string is invalid, else None.
    """
    error = None
    _smiles_dict = smiles_dict_from_yaml()
    path = os.path.join(dirs.data, "smiles_strings.yaml")

    if not is_valid_smiles(smiles_string):
        error = (
            f"Invalid SMILES string: {smiles_string}"
        )
        return error

    if group not in smiles_dict:
        _smiles_dict[group] = {}

    _smiles_dict[group][name] = smiles_string

    with open(path, "w") as f:
        yaml.dump(_smiles_dict, f)

    return error


def remove_molecule_from_dict(
    name: str,
) -> None | str:
    """
    Remove a molecule from the SMILES dictionary.

    Args:
        which contains molecule names as keys and SMILES strings as values.
        name (str): The name of the molecule to remove.
    Returns:
        error (str | None): Error message if molecule not found, else None.
    """
    _smiles_dict = smiles_dict_from_yaml()
    path = os.path.join(dirs.data, "smiles_strings.yaml")
    found = False
    error = None

    for group in _smiles_dict:
        if name in _smiles_dict[group]:
            del _smiles_dict[group][name]
            found = True
            break

    if not found:
        error = (
            f"Molecule {name} not found in the dictionary."
        )
        return error

    with open(path, "w") as f:
        yaml.dump(_smiles_dict, f)

    return error


if __name__ == "__main__":
    smiles_dict = smiles_dict_from_yaml()
    print(verify_entries(smiles_dict))
    add_molecule_to_dict(name="Test molecule", smiles_string="CCO", group="solvents")
    print(smiles_dict_from_yaml())
    remove_molecule_from_dict(name="Test molecule")
    print(smiles_dict_from_yaml())

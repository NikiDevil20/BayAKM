"""Contains the DirPaths Class."""
import os
from pathlib import Path
import re

import yaml


class DirPaths:
    """Class for handling the paths inside the module."""
    def __init__(self):
        self.base_dir = Path(__file__).resolve().parents[2]
        self.folder_path = None

        self.environ = os.path.join(self.base_dir, "src\\environment\\paths.yaml")
        self.data = os.path.join(self.base_dir, "data")
        self.smiles = os.path.join(self.base_dir, "src\\logic\\smiles\\smiles_strings.yaml")

        if not os.path.exists(self.data):
            os.makedirs(self.data)

    def build_campaign_folder(self, campaign_name):
        self.folder_path = os.path.join(
            self.data,
            cleanup_folder_name(campaign_name)
        )

        if not os.path.exists(self.folder_path):
            os.makedirs(self.folder_path)

        self.save_dir_to_file("folder", self.folder_path)
        self.save_dir_to_file("config", os.path.join(self.folder_path, "config.yaml"))
        self.save_dir_to_file("output", os.path.join(self.folder_path, "results.csv"))
        self.save_dir_to_file("parameters", os.path.join(self.folder_path, "parameters.yaml"))
        self.save_dir_to_file("campaign", os.path.join(self.folder_path, "campaign.yaml"))

    def set_bayakm_dir(self):
        self.save_dir_to_file("base", Path(__file__).resolve().parents[2])

    def save_dir_to_file(self, name: str, path: str | Path):
        yaml_dict = self.load_dirs_dict()
        yaml_dict[name] = path
        self.save_dict(yaml_dict)

    def load_dirs_dict(self) -> dict[str, str]:
        try:
            with open(self.environ) as f:
                yaml_dict = yaml.safe_load(f)
        except FileNotFoundError:
            yaml_dict = {}
        return yaml_dict

    def save_dict(self, yaml_dict: dict[str, str]):
        try:
            with open(self.environ, "w") as f:
                yaml.dump(yaml_dict, f)
        except FileNotFoundError:
            print(f"No file found at {self.environ}")

    def return_file_path(self, name):
        try:
            with open(self.environ, "r") as f:
                return yaml.safe_load(f)[name]
        except FileNotFoundError:
            print(f"Failed to open file at {self.environ}")

    @staticmethod
    def check_path(path):
        return os.path.exists(path)


# KI generiert:
def cleanup_folder_name(name: str) -> str:
    # Verbotene Zeichen für Windows und macOS
    forbidden = r'[\\/:*?"<>|]'
    # Reservierte Namen (Windows)
    reserved = {
        "CON", "PRN", "AUX", "NUL",
        *(f"COM{i}" for i in range(1, 10)),
        *(f"LPT{i}" for i in range(1, 10)),
    }
    # Zeichen ersetzen
    cleaned = re.sub(forbidden, "_", name)
    # Name kürzen
    cleaned = cleaned[:255]
    # Reservierte Namen vermeiden
    if cleaned.upper() in reserved:
        cleaned = f"_{cleaned}"
    # Leere Namen vermeiden
    if not cleaned.strip():
        cleaned = "folder"
    return cleaned


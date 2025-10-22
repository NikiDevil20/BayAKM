import os
from pathlib import Path

import yaml
from PySide6.QtWidgets import (QMainWindow, QStackedWidget,
                               QWizard, QLineEdit, QPushButton,
                               QFileDialog, QComboBox, QCheckBox,
                               QSizePolicy, QDialog, QFrame, QHBoxLayout,
                               QWidget, QVBoxLayout, QLabel, QTableWidget)
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile, QIODevice, QTimer, Qt
from PySide6.QtGui import QPixmap

from src.gui.pyside_gui.new_campaign_wizard import names_list
from src.gui.pyside_gui.ui_utilities import find_widget, add_widget_to_frame, save_or_load_envvars, save_config
from src.gui.pyside_gui.widget_classes import CounterWidget, CreateChoiceTable

name_list = [
    "NameLineEdit",
    "ChoiceList",
    "CreateOwnList"
]


class NewSubstanceParameter(QDialog):
    def __init__(self, ui_file_name="add_substance_parameter.ui"):
        super().__init__()

        self.ui_file_name = ui_file_name
        self.value_dict = {}
        self.parameter = None
        self.smiles_dict = None
        self.choice_table = None

        self._initialize_ui(self.ui_file_name)
        self._build_smiles_dict()
        self._build_choice_list()

    def get_values(self):
        return None

    def _initialize_ui(self, ui_file_name):
        file = QFile(ui_file_name)
        loader = QUiLoader()
        file.open(QFile.ReadOnly)  # Type: ignore
        self.dialog: QDialog = loader.load(file)
        file.close()

    def _build_smiles_dict(self):
        base_dir = Path(__file__).resolve().parents[3]
        file_path = os.path.join(base_dir, "src\\gui\\pyside_gui\\substances.yaml")

        with open(file_path) as f:
            yaml_string = f.read()

        self.smiles_dict = yaml.safe_load(yaml_string)

    def _build_choice_list(self):
        keys_sorted = list(self.smiles_dict.keys())
        keys_sorted.sort()

        self.choice_table = CreateChoiceTable(keys_sorted)

        add_widget_to_frame(self.dialog, "ChoiceListFrame", self.choice_table)

    def _collect_entries(self):
        name_list_from_choice_list = self.choice_table.get_selected()

        dict_from_choice = {}
        for choosen in name_list_from_choice_list:
            dict_from_choice[choosen] = self.smiles_dict[choosen]





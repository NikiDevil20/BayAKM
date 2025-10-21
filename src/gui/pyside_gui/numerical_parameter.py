from PySide6.QtWidgets import (QMainWindow, QStackedWidget,
                               QWizard, QLineEdit, QPushButton,
                               QFileDialog, QComboBox, QCheckBox,
                               QSizePolicy, QDialog)
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile, QIODevice, QTimer
from PySide6.QtGui import QPixmap

from src.gui.pyside_gui.ui_utilities import find_widget, add_widget_to_frame, save_or_load_envvars, save_config
from src.gui.pyside_gui.widget_classes import CounterWidget


class NewNumericalParameter(QDialog):
    def __init__(self, ui_file_name="add_numerical_parameter.ui"):
        super().__init__()

        self.ui_file_name = ui_file_name

        self._initialize_ui(self.ui_file_name)

    def _initialize_ui(self, ui_file_name):
        file = QFile(ui_file_name)
        loader = QUiLoader()
        file.open(QFile.ReadOnly)  # Type: ignore
        self.wizard: QWizard = loader.load(file)
        file.close()

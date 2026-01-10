from PySide6.QtWidgets import (QMainWindow, QStackedWidget,
                               QWizard, QLineEdit, QPushButton,
                               QFileDialog, QComboBox, QCheckBox,
                               QSizePolicy, QDialog)
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile, QIODevice, QTimer, Signal
from PySide6.QtGui import QPixmap


from src.gui.pyside_gui.ui_utilities import find_widget, add_widget_to_frame, save_or_load_envvars, save_config
from src.gui.pyside_gui.widget_classes import CounterWidget

names = [
    "param_name_lineedit",
    "param_values_lineedit"
]


class NewNumericalParameter(QDialog):
    parameter_created = Signal(object)

    def __init__(
            self,
            parent=None,
            ui_file_name="add_numerical_parameter.ui"
    ):
        super().__init__(parent)

        self.ui_file_name = ui_file_name
        self.value_dict = {}
        self.parameter = None

        self._initialize_ui(self.ui_file_name)
        self._connect_ok_btn()

    def _initialize_ui(self, ui_file_name):
        file = QFile(ui_file_name)
        loader = QUiLoader()
        file.open(QFile.ReadOnly)  # Type: ignore
        self.dialog = loader.load(file, self)
        file.close()

    def get_values(self):
        return self.parameter

    def _collect_entries(self):
        name_lineedit = find_widget(self.dialog, "param_name_lineedit")
        value_lineedit = find_widget(self.dialog, "param_values_lineedit")

        name = name_lineedit.text()
        value_string = value_lineedit.text()

        value_list = []
        for value in value_string.split(","):
            try:
                value_list.append(float(value.strip()))
            except ValueError:
                print("Could not convert value to float")

        if not self._verify_entries(name, value_list):
            NotImplementedError("Not implemented")

        from baybe.parameters import NumericalDiscreteParameter

        self.parameter = NumericalDiscreteParameter(
            name=name,
            values=tuple(value_list),
        )

        self.parameter_created.emit(self.parameter)
        self.dialog.accept()



    @staticmethod
    def _verify_entries(name, values):
        return True

    def _connect_ok_btn(self):
        self.dialog.ok_cancel_button.accepted.connect(self._collect_entries)


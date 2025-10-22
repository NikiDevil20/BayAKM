from PySide6.QtWidgets import (QMainWindow, QStackedWidget,
                               QWizard, QLineEdit, QPushButton,
                               QFileDialog, QComboBox, QCheckBox,
                               QSizePolicy)
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile, QIODevice, QTimer
from PySide6.QtGui import QPixmap

from src.gui.pyside_gui.ui_utilities import find_widget, add_widget_to_frame, save_or_load_envvars, save_config, \
    connect_widget, window_factory, widget_connect_command
from src.gui.pyside_gui.widget_classes import CounterWidget
from src.gui.pyside_gui.numerical_parameter import NewNumericalParameter

PATH_WATERMARK = "testtubes_small.jpg"
PLACEHOLDER_CAMPAIGN = "My first Campaign"
LINE_STYLE = "background-color: #FFFFFF"
registry = {
    "numerical": NewNumericalParameter
}
names_list = [
    "AddNum",
    "AddSubst"
]


class NewCampaignWizard(QWizard):
    def __init__(self, ui_file_name: str = "new_campaign_wizard.ui"):
        super().__init__()

        self.ui_file_name = ui_file_name
        self.wizard: QWizard | None = None
        self.child_list = []
        self.parameter_list = []

        self._initialize_ui(ui_file_name)
        self._wizard_setup()
        self._fill_content()
        self._initialize_next_button()
        self._connect_buttons()

    def _initialize_ui(self, ui_file_name):
        file = QFile(ui_file_name)
        loader = QUiLoader()
        file.open(QFile.ReadOnly)  # Type: ignore
        self.wizard: QWizard = loader.load(file)
        file.close()

    def _initialize_next_button(self):
        QTimer.singleShot(0, self._update_next_button)
        next_btn = self.wizard.button(QWizard.NextButton)
        next_btn.clicked.connect(self._on_next_klicked)

    def _wizard_setup(self):
        self.wizard.setWizardStyle(QWizard.ModernStyle)
        self.wizard.setPixmap(QWizard.WatermarkPixmap, QPixmap(PATH_WATERMARK))

    def _fill_content(self):
        self._setup_campaign_name()
        self._setup_folder_browser()
        self._setup_batchsize()
        self._setup_acquisition()
        self._setup_initial()
        self._setup_simulate()

    def _setup_campaign_name(self):
        self.campaign_line = QLineEdit()
        self.campaign_line.setPlaceholderText(PLACEHOLDER_CAMPAIGN)
        self.campaign_line.setStyleSheet(LINE_STYLE)
        add_widget_to_frame(
            window=self.wizard,
            frame_name="CampaignNameFrame",
            widget=self.campaign_line
        )
        self.campaign_line.textChanged.connect(self._update_next_button)

    def _setup_folder_browser(self):
        self.path_line = QLineEdit()
        self.path_line.setStyleSheet(LINE_STYLE)
        self.path_line.setReadOnly(True)
        add_widget_to_frame(
            window=self.wizard,
            frame_name="FolderFrameLineEdit",
            widget=self.path_line
        )

        browse_button = QPushButton()
        browse_button.setToolTip("Create a new folder for the new campaign.")
        browse_button.setText("browse...")
        browse_button.clicked.connect(self._on_browse_folder)

        add_widget_to_frame(
            window=self.wizard,
            frame_name="FolderFrameBrowseButton",
            widget=browse_button
        )
        self.path_line.textChanged.connect(self._update_next_button)

    def _on_browse_folder(self):
        parent = self.wizard if isinstance(self.wizard, QWizard) else self
        path = QFileDialog.getExistingDirectory(parent, "Choose folder", "")
        if path:
            if self.path_line is not None:
                self.path_line.setText(path)

    def _setup_batchsize(self):
        self.batchsize = CounterWidget()
        add_widget_to_frame(
            window=self.wizard,
            frame_name="BatchSizeFrame",
            widget=self.batchsize
        )

    def _setup_acquisition(self):
        self.acqf_box = QComboBox()
        self.acqf_box.setStyleSheet(LINE_STYLE)
        self.acqf_box.addItems([
            "qLogEI",
            "qPI",
            "UCB"
        ])

        add_widget_to_frame(
            window=self.wizard,
            frame_name="AcquisitionFrame",
            widget=self.acqf_box
        )

    def _setup_initial(self):
        self.initial_box = QComboBox()
        self.initial_box.setStyleSheet(LINE_STYLE)
        self.initial_box.addItems([
            "FPS",
            "Random",
        ])

        add_widget_to_frame(
            window=self.wizard,
            frame_name="InitialRecommenderFrame",
            widget=self.initial_box
        )

    def _setup_simulate(self):
        self.simulate = QCheckBox()

        add_widget_to_frame(
            window=self.wizard,
            frame_name="SimulateFrame",
            widget=self.simulate
        )

    def _verify_entries(self) -> None | str:
        # Campaign name:
        self.campaign_name = self.campaign_line.text()
        self.campaign_name = self.campaign_name.strip()
        if self.campaign_name == "":
            return "Must set campaign name."

        # Campaign path:
        self.campaign_path = self.path_line.text()
        if self.campaign_path == "":
            return "Must set campaign path."

        return None

    def _on_next_klicked(self):
        error_check = self._verify_entries()
        if error_check is not None:
            print(error_check)

        self.entries_dict = self._collect_entries()
        self.envvars_dict = save_or_load_envvars(self.entries_dict)
        save_config(self.entries_dict)

    def _update_next_button(self):
        next_btn = self.wizard.button(QWizard.NextButton)

        is_ok = self._verify_entries() is None
        next_btn.setEnabled(is_ok)

    def _collect_entries(self) -> dict[str, str | int | bool]:
        entries_dict = {
            "campaign_name": self.campaign_line.text(),
            "campaign_path": self.path_line.text(),
            "batchsize": self.batchsize.value(),
            "initial_recommender": self.initial_box.currentText(),
            "acquisition_function": self.acqf_box.currentText(),
            "simulate_results": self.simulate.isChecked()
        }
        return entries_dict

    def _open_dialog(self, name):
        new_dialog = window_factory(name)
        new_dialog.dialog.exec()

        new_parameter = new_dialog.get_values()
        self.parameter_list.append(new_parameter)

    def _connect_buttons(self):
        for name in names_list:
            widget_connect_command(
                widget_name=name,
                window=self.wizard,
                func=lambda: self._open_dialog(name),
            )


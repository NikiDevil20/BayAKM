from PySide6.QtWidgets import (QMainWindow, QStackedWidget,
                               QWizard, QLineEdit, QPushButton,
                               QFileDialog, QComboBox, QCheckBox,
                               QSizePolicy)
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile, QIODevice, QTimer
from PySide6.QtGui import QPixmap

from src.gui.pyside_gui.ui_utilities import find_widget, add_widget_to_frame
from src.gui.pyside_gui.widget_classes import CounterWidget

frame_list = [

]
PATH_WATERMARK = "testtubes_small.jpg"
PLACEHOLDER_CAMPAIGN = "My first Campaign"
LINE_STYLE = "background-color: #FFFFFF"

class NewCampaignWizard(QWizard):
    def __init__(self, parent=None, ui_file_name: str = "new_campaign_wizard.ui"):
        super().__init__(parent)
        self.ui_file_name = ui_file_name
        self.wizard: QWizard | None = None
        self.path_line: QLineEdit | None = None

        file = QFile(ui_file_name)
        loader = QUiLoader()
        file.open(QFile.ReadOnly)  # Type: ignore
        self.wizard: QWizard = loader.load(file)
        file.close()

        self._wizard_setup()

        QTimer.singleShot(0, self._update_next_button)

    def _wizard_setup(self):
        self.wizard.setWizardStyle(QWizard.ModernStyle)
        self.wizard.setPixmap(QWizard.WatermarkPixmap, QPixmap(PATH_WATERMARK))

        self._setup_campaign_name()
        self._setup_folder_browser()
        self._setup_batchsize()
        self._setup_acquisition()
        self._setup_initial()
        self._setup_simulate()

    def _page_setup(self):
        self.page1 = self.wizard.settings
        self.page2 = self.wizard.parameters

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
        else:
            print("No errors")

    def _update_next_button(self, *args):
        next_btn = self.wizard.button(QWizard.NextButton)

        is_ok = self._verify_entries() is None
        print(f"is ok: {is_ok}")
        next_btn.setEnabled(is_ok)

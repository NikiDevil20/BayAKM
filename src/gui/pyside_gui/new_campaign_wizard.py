from PySide6.QtWidgets import (QMainWindow, QStackedWidget,
                               QWizard, QLineEdit, QPushButton,
                               QFileDialog)
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile, QIODevice
from PySide6.QtGui import QPixmap

from src.gui.pyside_gui.ui_utilities import find_widget, add_widget_to_frame

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
        self.page1 = None
        self.page2 = None
        self.path_line: QLineEdit | None = None

        file = QFile(ui_file_name)

        loader = QUiLoader()
        file.open(QFile.ReadOnly)  # Type: ignore

        self.wizard: QWizard = loader.load(file)
        file.close()
        # self._page_setup()
        self._wizard_setup()

    def _wizard_setup(self):
        self.wizard.setWizardStyle(QWizard.ModernStyle)
        self.wizard.setPixmap(QWizard.WatermarkPixmap, QPixmap(PATH_WATERMARK))

        self._setup_campaign_name()
        self._setup_folder_browser()

    def _page_setup(self):
        self.page1 = self.wizard.settings
        self.page2 = self.wizard.parameters

    def _setup_campaign_name(self):
        campaign_line = QLineEdit()
        campaign_line.setPlaceholderText(PLACEHOLDER_CAMPAIGN)
        campaign_line.setStyleSheet(LINE_STYLE)
        add_widget_to_frame(
            window=self.wizard,
            frame_name="CampaignNameFrame",
            widget=campaign_line
        )

    def _setup_folder_browser(self):
        self.path_line = QLineEdit()
        self.path_line.setStyleSheet(LINE_STYLE)
        add_widget_to_frame(
            window=self.wizard,
            frame_name="FolderFrameLineEdit",
            widget=self.path_line
        )

        browse_button = QPushButton()
        browse_button.setToolTip("browse...")
        browse_button.clicked.connect(self._on_browse_folder)

        add_widget_to_frame(
            window=self.wizard,
            frame_name="FolderFrameBrowseButton",
            widget=browse_button
        )

    def _on_browse_folder(self):
        parent = self.wizard if isinstance(self.wizard, QWizard) else self
        path = QFileDialog.getExistingDirectory(parent, "Choose folder", "")
        if path:
            if self.path_line is not None:
                self.path_line.setText(path)

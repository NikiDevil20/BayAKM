from PySide6.QtWidgets import QMainWindow, QStackedWidget
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile, QIODevice

from src.gui.pyside_gui.ui_utilities import find_widget


class NewCampaignWindow(QMainWindow):
    def __init__(self, parent=None, ui_file_name: str = "new_campaign.ui"):
        super().__init__(parent)
        self.ui_file_name = ui_file_name
        self.app = None
        self.window = None
        self.parent = parent

        file = QFile(ui_file_name)

        loader = QUiLoader()
        file.open(QFile.ReadOnly)  # Type: ignore

        self.window = loader.load(file)
        file.close()

        self.setup()

    def setup(self):
        stack: QStackedWidget = find_widget(self.window, "stackedWidget")
        stack.setCurrentIndex(1)

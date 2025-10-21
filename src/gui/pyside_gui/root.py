import sys
from typing import Callable

from PySide6.QtWidgets import QApplication, QWidget, QMainWindow, QPushButton
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile, QIODevice

from src.gui.pyside_gui.ui_utilities import connect_widget, open_window


class MainWindow(QMainWindow):
    def __init__(self, ui_file_name: str = "home.ui"):
        super().__init__()
        self.ui_file_name = QFile(ui_file_name)
        self.app = None
        self.window = None
        self.child_windows = []
        self.name_list = [
            "btn_new_campaign",
        ]

        file = QFile(ui_file_name)

        loader = QUiLoader()
        file.open(QFile.ReadOnly)  # Type: ignore

        self.window = loader.load(file)
        file.close()

        self.setup()

    def setup(self):
        connect_widget(
            self.window,
            self.name_list,
            self.child_windows
        )


if __name__ == "__main__":
    app = QApplication()
    main_window = MainWindow()
    window = main_window.window
    window.show()
    app.exec()


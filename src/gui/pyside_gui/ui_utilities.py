from typing import Callable
from PySide6.QtWidgets import QMainWindow, QStackedWidget, QWizard, QFrame, QWidget, QVBoxLayout


def btn_connect_command(window, btn_name: str, function: Callable) -> None:
    btn = find_widget(window, btn_name)
    btn.triggered.connect(function)


def find_widget(window, name):
    return window.__getattribute__(name)


def open_window(name, child_list):
    new_window: QMainWindow | QWizard = window_factory(name)
    if isinstance(new_window, QWizard):
        new_window.wizard.exec()
    elif isinstance(new_window, QMainWindow):
        new_window.window.show()
    child_list.append(new_window.window)
    return child_list


def window_factory(name: str):
    if name == "btn_new_campaign":
        from src.gui.pyside_gui.new_campaign_wizard import NewCampaignWizard
        window = NewCampaignWizard()
    else:
        raise ValueError(f" {name} name not found")
    return window


def add_widget_to_frame(window: QMainWindow | QWizard, frame_name: str, widget: QWidget):
    frame = find_widget(window, frame_name)
    layout = frame.layout()
    if layout is None:
        layout = QVBoxLayout(frame)
    layout.addWidget(widget)

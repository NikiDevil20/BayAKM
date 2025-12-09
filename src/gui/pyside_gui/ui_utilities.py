import os
import yaml
from pathlib import Path

from typing import Callable, Union, Iterable
from PySide6.QtWidgets import (QMainWindow, QStackedWidget,
                               QWizard, QFrame, QWidget, QHBoxLayout,
                               QVBoxLayout, QDialog, QPushButton)


def widget_connect_command(window, widget_name: str, func: Callable) -> None:
    widget = find_widget(window, widget_name)
    if isinstance(widget, QPushButton):
        widget.clicked.connect(func)
    else:
        widget.triggered.connect(func)


def find_widget(window, name):
    return window.__getattribute__(name)


def open_window(name, child_list):
    new_window: QMainWindow | QWizard = window_factory(name)
    if isinstance(new_window, QWizard) or isinstance(new_window, QDialog):
        new_window.wizard.exec()
    elif isinstance(new_window, QMainWindow):
        new_window.window.show()
    child_list.append(new_window.window)
    return child_list


def window_factory(name: str):
    if name == "btn_new_campaign":
        from src.gui.pyside_gui.new_campaign_wizard import NewCampaignWizard
        window = NewCampaignWizard()
    elif name == "AddNum":
        from src.gui.pyside_gui.numerical_parameter import NewNumericalParameter
        window = NewNumericalParameter()
    elif name == "AddSubst":
        from src.gui.pyside_gui.substance_parameter import NewSubstanceParameter
        window = NewSubstanceParameter()
    else:
        raise ValueError(f" {name} name not found")
    return window


def add_widget_to_frame(window: QMainWindow | QWizard, frame_name: str, widget: QWidget):
    frame = find_widget(window, frame_name)
    layout = frame.layout()
    if layout is None:
        layout = QVBoxLayout(frame)
    layout.setContentsMargins(0, 0, 0, 0)
    layout.setSpacing(6)
    layout.addWidget(widget)


def save_config(config_dict: dict[str, str | int | bool] = None) -> None:
    folder_path = config_dict["campaign_path"]
    full_path = os.path.join(folder_path, "config.yaml")

    with open(full_path, "w") as f:
        yaml.dump(config_dict, f)


def load_config(campaign_name: str = None) -> dict:
    folder_path = return_campaign_path(campaign_name)
    full_path = os.path.join(folder_path, "config.yaml")
    with open(full_path) as f:
        yaml_string = f.read()
    return yaml.safe_load(yaml_string)


def save_or_load_envvars(config_dict: dict = None) -> dict:
    base_dir = Path(__file__).resolve().parents[3]
    file_path = os.path.join(base_dir, "src\\gui\\pyside_gui\\envvars.yaml")

    # read
    if os.path.exists(file_path):
        with open(file_path) as f:
            yaml_string = f.read()
        envvars_dict = yaml.safe_load(yaml_string)
    else:
        envvars_dict = {}

    if config_dict is not None:
        folder_path = config_dict["campaign_path"]
        campaign_name = config_dict["campaign_name"]

        envvars_dict[campaign_name] = folder_path

    # write
    with open(file_path, "w") as f:
        yaml.dump(envvars_dict, f)

    return envvars_dict


def return_campaign_path(campaign_name: str = None) -> str:
    envvars_dict = save_or_load_envvars()
    if campaign_name is not None:
        return envvars_dict[campaign_name]

    latest_addition = next(reversed(envvars_dict))
    return envvars_dict[latest_addition]


def connect_widget(window, names: str | list[str], child_windows: list) -> list:
    """
    Connect widgets (single name or iterable of names) to handlers that open windows.
    Returns the (mutated) child_windows list.
    """
    if isinstance(names, str):
        names_iter = [names]
    else:
        names_iter = list(names)

    def _make_handler(n: str):
        def _handler(**_kwargs):
            open_window(n, child_windows)

        return _handler

    for name in names_iter:
        widget_connect_command(window, name, _make_handler(name))

    return child_windows

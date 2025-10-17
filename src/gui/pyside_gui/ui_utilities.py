from typing import Callable

def btn_connect_command(window, btn_name: str, function: Callable) -> None:
    btn = find_widget(window, btn_name)
    btn.triggered.connect(function)


def find_widget(window, name):
    return window.__getattribute__(name)


def open_window(name, child_list):
    new_window = window_factory(name)
    new_window.window.show()
    child_list.append(new_window.window)
    return child_list

def window_factory(name: str):
    if name == "btn_new_campaign":
        from src.gui.pyside_gui.new_campaign_frame import NewCampaignWindow
        window = NewCampaignWindow()
    else:
        raise ValueError(f" {name} name not found")
    return window
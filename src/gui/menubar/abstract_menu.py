import tkinter as tk
from typing import Callable

import customtkinter as ctk




class AbstractMenu:
    def __init__(
            self,
            master,
            entries: dict[str, Callable | None | dict]
    ):
        self.entries = entries
        self.menu = self._recursive_menu_builder(entries, master=master)

    def return_menu(self):
        return self.menu

    def _recursive_menu_builder(self, menu_dict, master):
        menu = tk.Menu(master)
        for key in menu_dict.keys():
            if key == "break":
                menu.add_separator()
                continue

            if not menu_dict[key]:
                menu.add_command(label=key, command=lambda: print(key))
                continue

            if isinstance(menu_dict[key], dict):
                submenu = self._recursive_menu_builder(menu_dict[key], master=menu)
                menu.add_cascade(label=key, menu=submenu)
                continue

            menu.add_command(label=key, command=menu_dict[key])

        return menu


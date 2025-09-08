import customtkinter as ctk

from src.bayakm.parameters import delete_parameter, build_param_list
from src.gui.gui_constants import STANDARD, TEXTCOLOR, FGCOLOR
from src.gui.new_page_factory import BaseFrame

HEADER_TEXT = "Remove parameters"
BUTTON_TEXT = "Remove"


class RemoveParameterFrame(BaseFrame):
    def __init__(self, master):
        super().__init__(master)

        self.parameter_list = build_param_list()
        self.checkbox_list = []

    def fill_content(self):
        self.header = HEADER_TEXT
        self.build_frames()

        self._display_parameter_checkboxes()

        remove_button = ctk.CTkButton(
            master=self.bottom_frame,
            text=BUTTON_TEXT,
            width=30,
            command=lambda: self._remove_parameter(),
            text_color=TEXTCOLOR,
            font=STANDARD,
            fg_color=FGCOLOR
        )
        remove_button.grid(row=0, column=0, pady=5, padx=10)

    def _display_parameter_checkboxes(self):
        for i, parameter in enumerate(self.parameter_list):
            checkbox = ctk.CTkCheckBox(
                master=self.content_frame,
                text=parameter.name,
                font=STANDARD
            )
            checkbox.grid(row=i, column=0, pady=2, padx=10, sticky="w")

            self.checkbox_list.append((checkbox, parameter.name))

    def _remove_parameter(self):
        parameters_list = [name for (checkbox, name) in self.checkbox_list if checkbox.get()]

        if len(parameters_list) > 0:
            delete_parameter(parameters_list)

        self.master.master.refresh_parameters()
        self.master.destroy()

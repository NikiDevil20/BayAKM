import customtkinter as ctk

from src.logic.parameters.parameters import write_to_parameters_file
from src.gui.main.gui_constants import STANDARD
from src.gui.help.help import error_subwindow
from src.gui.new_campaign_tabview.new_page_factory import BaseFrame

HEADER_PLACEHOLDER = "Add numerical parameter"
PARAMETER_NAME_PLACEHOLDER = "Parameter name"
VALUE_PLACEHOLDER = "Values"


class NewNumericalParameterFrame(BaseFrame):
    def __init__(self, master):
        super().__init__(master)
        self.name_entry = None
        self.content_entry = None

    def fill_content(self):
        self.header = HEADER_PLACEHOLDER
        self.build_frames()

        self.name_entry = ctk.CTkEntry(
            master=self.content_frame,
            placeholder_text=PARAMETER_NAME_PLACEHOLDER,
            font=STANDARD
        )
        self.name_entry.grid(row=1, column=0, pady=5, padx=10)

        self.content_entry = ctk.CTkEntry(
            master=self.content_frame,
            placeholder_text=VALUE_PLACEHOLDER,
            font=STANDARD
        )
        self.content_entry.grid(row=1, column=1, pady=5, padx=10)

        save_button = ctk.CTkButton(
            master=self.content_frame, text="Save", width=20,
            command=lambda: self._command_save_parameter(),
            font=STANDARD, text_color="black", fg_color="light blue"
        )
        save_button.grid(
            row=1, column=2,
            pady=5, padx=10
        )

        bottom_label = ctk.CTkLabel(
            master=self.bottom_frame,
            text=("Enter parameter name on the left and parameter"
                  "\n values, separated by comma, on the right."),
            font=STANDARD
        )

        bottom_label.grid(row=0, column=0, pady=5, padx=10)

    def _command_save_parameter(self):
        parameter_list = []
        for value in self.content_entry.get().split(","):
            try:
                parameter_list.append(float(value.strip()))
            except ValueError:
                error_subwindow(
                    master=self,
                    message=f"Value '{value.strip()}' could not be converted to float."
                )
                return

        if self.name_entry.get() == "":
            error_subwindow(
                self,
                message="Parameter name cannot be empty."
            )
            return

        parameter_list = list(set(parameter_list))

        if len(parameter_list) < 2:
            error_subwindow(
                self,
                message="Parameter needs to have at least two numerical values."
            )
            return

        error_msg = write_to_parameters_file(
            mode="numerical",
            parameter_name=self.name_entry.get(),
            parameter_values=parameter_list
        )
        if error_msg is not None:
            error_subwindow(self, error_msg)
            return

        self.master.master.refresh_parameters()
        self.master.destroy()

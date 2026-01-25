import customtkinter as ctk

from src.logic.parameters.parameters import write_to_parameters_file
from src.gui.main.gui_constants import STANDARD
from src.gui.help.help import error_subwindow
from src.gui.new_campaign_tabview.new_page_factory import BaseFrame

HEADER_PLACEHOLDER = "Add continuous parameter"
PARAMETER_NAME_PLACEHOLDER = "Parameter name"
LOWER = "Lower bound"
UPPER = "Upper bound"


class NewContinuousParameterFrame(BaseFrame):
    def __init__(self, master):
        super().__init__(master)
        self.name_entry = None
        self.upper_bound = None
        self.lower_bound = None

    def fill_content(self):
        self.header = HEADER_PLACEHOLDER
        self.build_frames()

        self.name_entry = ctk.CTkEntry(
            master=self.content_frame,
            placeholder_text=PARAMETER_NAME_PLACEHOLDER,
            font=STANDARD
        )
        self.name_entry.grid(row=1, column=0, pady=5, padx=10)

        self.lower_bound = ctk.CTkEntry(
            master=self.content_frame,
            placeholder_text=LOWER,
            font=STANDARD,
        )
        self.lower_bound.grid(row=1, column=1, pady=5, padx=10)
        self.upper_bound = ctk.CTkEntry(
            master=self.content_frame,
            placeholder_text=UPPER,
            font=STANDARD
        )
        self.upper_bound.grid(row=1, column=2, pady=5, padx=10)

        save_button = ctk.CTkButton(
            master=self.content_frame, text="Save", width=20,
            command=lambda: self._command_save_parameter(),
            font=STANDARD, text_color="black", fg_color="light blue"
        )
        save_button.grid(
            row=1, column=3,
            pady=5, padx=10
        )

        bottom_label = ctk.CTkLabel(
            master=self.bottom_frame,
            text="Enter parameter name on the left and parameter bounds on the right.",
            font=STANDARD
        )

        bottom_label.grid(row=0, column=0, pady=5, padx=10)

    def _command_save_parameter(self):
        lower = self.check_and_convert(self.lower_bound.get())
        upper = self.check_and_convert(self.upper_bound.get())

        if abs(upper - lower) < 0.001:
            error_subwindow(self, f"Lower ({lower}) and upper value ({upper}) must not be equal.")
            return

        bounds = [lower, upper]

        # Appending list of parameter to the parameters.yaml file.
        error_msg = write_to_parameters_file(
            mode="continuous",
            parameter_name=self.name_entry.get(),
            parameter_values=bounds
        )
        if error_msg is not None:
            error_subwindow(self, error_msg)
            return

        # Refreshing the displayed parameters in the new campaign tabview
        # and destroy the new_parameter frame.
        self.master.master.refresh_parameters()
        self.master.destroy()

    def check_and_convert(self, value) -> float:
        try:
            return float(value)
        except TypeError:
            error_subwindow(self, f"Cannot convert entry '{value}' to float.")

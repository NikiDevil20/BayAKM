import customtkinter as ctk

from src.bayakm.parameters import write_to_parameters_file
from src.gui.help import error_subwindow
from src.gui.gui_constants import *


class AddNumericalFrame(ctk.CTkFrame):
    def __init__(self, master=None):
        super().__init__(master)

        # Building frame's content
        self._create_header()
        self._create_content_frame()
        self._create_bottom_frame()

    def _create_header(self):
        """Building the frame's header.
        """
        header_frame = ctk.CTkFrame(master=self)
        header_frame.grid(
            row=0, column=0,
            pady=5, padx=10,
            sticky="ew"
        )
        header = ctk.CTkLabel(
            master=header_frame,
            text="Add new numerical parameter",
            font=HEADER
        )
        header.pack(pady=10, padx=30)

    def _create_content_frame(self):
        """Main content frame: Entries are placed here.
        """
        content_frame = ctk.CTkFrame(master=self)
        content_frame.grid(
            row=1, column=0,
            pady=5, padx=10,
            sticky="ew")

        # Entry for parameter name.
        self.name_entry = ctk.CTkEntry(
            master=content_frame,
            placeholder_text="Parameter name"
        )
        self.name_entry.grid(
            row=1, column=0,
            pady=5, padx=10
        )

        # Entry for parameter values.
        self.content_entry = ctk.CTkEntry(
            master=content_frame,
            placeholder_text="Values"
        )
        self.content_entry.grid(
            row=1, column=1,
            pady=5, padx=10
        )

        # Button to save the new parameter.
        save_button = ctk.CTkButton(
            master=content_frame, text="Save", width=20,
            command=lambda: self._command_save_parameter()
        )
        save_button.grid(
            row=1, column=2,
            pady=5, padx=10
        )

    def _create_bottom_frame(self):
        """Frame below the content frame, which
        contains an explanation.
        """
        bottom_frame = ctk.CTkFrame(master=self)
        bottom_frame.grid(
            row=2, column=0,
            pady=5, padx=10,
            sticky="ew"
        )

        bottom_label = ctk.CTkLabel(
            master=bottom_frame,
            text=("Enter parameter name on the left and parameter"
                  "\n values, separated by comma, on the right.")
        )
        bottom_label.pack(pady=5, padx=10)

    def _command_save_parameter(self):
        # Sehr schöne list comprehension, in die leider kein error handling passt :(
        # parameter_list = [float(value) for value in self.content_entry.get().split(", ")]

        parameter_list = []
        # Appending the comma separated values in the entry to the parameter_list.
        for value in self.content_entry.get().split(","):
            try:
                parameter_list.append(float(value.strip()))  # Strip off spaces and try to convert value to float.
            except ValueError:  # Call error subwindow if value cannot be converted to float.
                error_subwindow(
                    master=self,
                    message=f"Value '{value.strip()}' could not be converted to float."
                )
                return

        if self.name_entry.get() == "":  # Call error subwindow if name is empty.
            error_subwindow(
                self,
                message="Parameter name cannot be empty."
            )
            return

        if len(parameter_list) < 2:  # Call error subwindow if only one parameter is detected.
            error_subwindow(
                self,
                message="Parameter needs to have at least two numerical values."
            )
            return

        # Appending list of parameter to the parameters.yaml file.
        write_to_parameters_file(
            mode="numerical",
            parameter_name=self.name_entry.get(),
            parameter_values=parameter_list
        )

        # Refreshing the displayed parameters in the new campaign tabview
        # and destroy the new_parameter frame.
        self.master.master.refresh_parameters()
        self.master.destroy()

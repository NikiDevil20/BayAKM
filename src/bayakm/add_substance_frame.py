import customtkinter as ctk
from src.bayakm.parameters import write_to_parameters_file


class AddSubstanceFrame(ctk.CTkFrame):
    def __init__(self, master=None):
        super().__init__(master)

        header_frame = ctk.CTkFrame(master=self)
        header_frame.grid(row=0, column=0, pady=5, padx=10, sticky="ew")
        header = ctk.CTkLabel(master=header_frame, text="Add new substance parameter", font=("Arial", 24))
        header.pack(pady=10, padx=30)

        content_frame = ctk.CTkFrame(master=self)
        content_frame.grid(row=1, column=0, pady=5, padx=10, sticky="ew")

        self.name_entry = ctk.CTkEntry(master=content_frame, placeholder_text="Parameter name")
        self.name_entry.grid(row=1, column=0, pady=5, padx=10)

        self.content_entry = ctk.CTkEntry(master=content_frame, placeholder_text="Values")
        self.content_entry.grid(row=1, column=1, pady=5, padx=10)

        safe_button = ctk.CTkButton(master=content_frame, text="Save", width=20, command=lambda: self._save_parameter())
        safe_button.grid(row=1, column=2, pady=5, padx=10)

        bottom_frame = ctk.CTkFrame(master=self)
        bottom_frame.grid(row=2, column=0, pady=5, padx=10, sticky="ew")

        bottom_label = ctk.CTkLabel(
            master=bottom_frame,
            text="Enter parameter name on the left and parameter \n values, separated by comma, on the right."
        )
        bottom_label.pack(pady=5, padx=10)

    def _save_parameter(self):
        parameter_name = self.name_entry.get()
        content_string = self.content_entry.get()
        parameter_list: list[float] = []
        for value in content_string.split(", "):
            parameter_list.append(float(value))
        write_to_parameters_file(mode="numerical", parameter_name=parameter_name, parameter_values=parameter_list)
        self.master.master._refresh_parameters()
        self.master.destroy()
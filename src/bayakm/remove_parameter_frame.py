import customtkinter as ctk
from src.bayakm.parameters import delete_parameter, build_param_list


class RemoveParameterFrame(ctk.CTkFrame):
    def __init__(self, master=None):
        super().__init__(master)

        content_frame = ctk.CTkFrame(master=self)
        content_frame.pack(pady=5, padx=10)
        self.parameter_list = build_param_list()
        self.checkbox_list = []
        for i, parameter in enumerate(self.parameter_list):
            checkbox = ctk.CTkCheckBox(master=content_frame, text=parameter.name)
            checkbox.grid(row=i, column=0, pady=2, padx=10, sticky="w")
            self.checkbox_list.append((checkbox, parameter.name))

        remove_button = ctk.CTkButton(
            master=self, text="Remove", width=30, command=lambda: self._remove_parameter(), text_color="black")
        remove_button.pack(pady=10, padx=10)

    def _remove_parameter(self):
        parameters_list = []
        for (checkbox, name) in self.checkbox_list:
            if checkbox.get():
                parameters_list.append(name)
        if len(parameters_list) > 0:
            delete_parameter(parameters_list)
        self.master.master.refresh_parameters()
        self.master.destroy()

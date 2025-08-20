import customtkinter as ctk

from src.bayakm.parameters import write_to_parameters_file
from src.gui.help import error_subwindow


class AddSubstanceFrame(ctk.CTkFrame):
    def __init__(self, master=None):
        super().__init__(master)

        self.row_list = []

        self._create_header_frame()
        self._create_content_frame()
        self._create_bottom_frame()

    def _create_header_frame(self):
        header_frame = ctk.CTkFrame(master=self)
        header_frame.grid(
            row=0, column=0,
            pady=5, padx=10,
            sticky="ew"
        )
        header = ctk.CTkLabel(
            master=header_frame,
            text="Add new substance parameter",
            font=("Arial", 24)
        )
        header.pack(pady=10, padx=30)

    def _create_content_frame(self):
        self.content_frame = ctk.CTkScrollableFrame(
            master=self,
            height=200,
        )
        self.content_frame.grid(
            row=1, column=0,
            pady=5, padx=10,
            sticky="ew"
        )

        self.name_entry = ctk.CTkEntry(
            master=self.content_frame,
            placeholder_text="Parameter name"
        )
        self.name_entry.grid(
            row=0, column=0,
            pady=5, padx=10
        )

        self._create_row()
        self._create_row()

    def _create_row(self):
        i = len(self.row_list) + 1

        row = ctk.CTkFrame(master=self.content_frame)
        row.grid(
            row=i, column=0,
            pady=5, padx=10,
            sticky="ew", columnspan=2
        )

        substance_name_entry = ctk.CTkEntry(
            master=row,
            placeholder_text="Substance name"
        )
        smiles_entry = ctk.CTkEntry(
            master=row,
            placeholder_text="SMILES string"
        )

        substance_name_entry.grid(
            row=0, column=0,
            pady=5, padx=10
        )
        smiles_entry.grid(
            row=0, column=1,
            pady=5, padx=10
        )

        self._remove_button(row)

        self.row_list.append((substance_name_entry, smiles_entry))

    @staticmethod
    def _remove_button(master):
        remove_button = ctk.CTkButton(
            master=master,
            text="-",
            command=lambda: master.destroy(),
            width=10
        )
        remove_button.grid(
            row=0, column=2,
            pady=5, padx=10
        )

    def _create_bottom_frame(self):
        bottom_frame = ctk.CTkFrame(master=self)
        bottom_frame.grid(
            row=2, column=0,
            pady=5, padx=10,
            sticky="ew"
        )

        save_button = ctk.CTkButton(
            master=bottom_frame,
            text="Save",
            width=20,
            command=lambda: self._command_save_parameter()
        )
        save_button.grid(
            row=0, column=1,
            pady=5, padx=10
        )
        add_button = ctk.CTkButton(
            master=bottom_frame,
            text="+",
            command=lambda: self._create_row(),
            width=10
        )
        add_button.grid(
            row=0, column=0,
            pady=5, padx=10
        )

    def _command_save_parameter(self):
        if self.name_entry.get() == "":
            error_subwindow(
                self,
                message="Parameter name cannot be empty."
            )
            return
        substance_dict: dict[str, str] = {}

        for (substance_name_entry, smiles_entry) in self.row_list:
            if substance_name_entry.get() == "" or smiles_entry.get() == "":
                continue
            substance_dict[substance_name_entry.get()] = smiles_entry.get()

        if len(substance_dict.keys()) < 2:
            error_subwindow(
                self,
                message="You must add at least two values to a parameter."
            )
            return

        write_to_parameters_file(
            mode="substance",
            parameter_name=self.name_entry.get(),
            parameter_values=substance_dict
        )

        self.master.master.refresh_parameters()
        self.master.destroy()

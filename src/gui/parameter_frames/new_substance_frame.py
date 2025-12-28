import customtkinter as ctk

from src.bayakm.parameters import write_to_parameters_file
from src.gui.main_gui.gui_constants import STANDARD, FGCOLOR, TEXTCOLOR, ROWFGCOLOR
from src.gui.help import error_subwindow
from src.gui.main_gui.new_page_factory import BaseFrame
from src.bayakm.smiles_loader import (smiles_dict_from_yaml, verify_entries, add_molecule_to_dict,
                                      remove_molecule_from_dict, smiles_type)

HEADER_TEXT = "New Substance Parameter"
PARAMNAME_PLACEHOLDER = "Parameter name"
SMILES_PLACEHOLDER = "Smiles string"
SUBSTNAME_PLACEHOLDER = "Substance name"


class NewSubstanceParameterFrame(BaseFrame):
    def __init__(self, master):
        super().__init__(master)
        self.row_list = []
        self.name_entry = None
        self.row_frame = None
        self.list_frame = None

    def _create_row(self):
        """Creates a row with two entries for substance name and SMILES string.
        Rows can be added and removed via button press.
        """
        row = ctk.CTkFrame(master=self.row_frame, fg_color=ROWFGCOLOR)
        for col in range(2):
            row.columnconfigure(col, weight=1)
        row.grid(
            row=len(self.row_list) + 1, column=0,
            pady=5, padx=10,
            sticky="ew", columnspan=2
        )

        substance_name_entry = ctk.CTkEntry(
            master=row,
            placeholder_text=SUBSTNAME_PLACEHOLDER,
            font=STANDARD,
            width=150
        )
        smiles_entry = ctk.CTkEntry(
            master=row,
            placeholder_text=SMILES_PLACEHOLDER,
            font=STANDARD,
            width=100
        )

        substance_name_entry.grid(row=0, column=0, pady=5, padx=10)
        smiles_entry.grid(row=0, column=1, pady=5, padx=10)

        # Add one remove button per row,
        # which removes it upon click.
        remove_button = ctk.CTkButton(
            master=row,
            text="-",
            command=lambda: self._delete_row(row, (substance_name_entry, smiles_entry)),
            width=10,
            fg_color=FGCOLOR,
            text_color=TEXTCOLOR
        )
        remove_button.grid(row=0, column=2, pady=5, padx=10)

        # Row's entries are placed in a list,
        # so their values can be retrieved.
        self.row_list.append((substance_name_entry, smiles_entry))

    def _delete_row(self, row, entry_tuple):
        row.destroy()
        self.row_list.remove(entry_tuple)

    def _command_save_parameter(self):
        """Method for saving the parameter's name and values.
        The SMILES string is checked by the BayBE package
        upon parameter generation by the build_parameter_list()
        function in the parameters.py file.
        """

        if self.name_entry.get() == "":  # Name cannot be empty.
            error_subwindow(
                self,
                message="Parameter name cannot be empty."
            )
            return

        substance_dict: dict[str, str] = {}

        for (substance_name_entry, smiles_entry) in self.row_list:
            # Substance name and SMILES string must not be empty.
            if substance_name_entry.get() == "" or smiles_entry.get() == "":
                continue
            substance_dict[substance_name_entry.get()] = smiles_entry.get()

        if len(substance_dict.keys()) < 2:  # At least two values are needed for parameter creation.
            error_subwindow(
                self,
                message="You must add at least two values to a parameter."
            )
            return

        # The new parameter is added to the parameters.yaml file.
        error_msg = write_to_parameters_file(
            mode="substance",
            parameter_name=self.name_entry.get(),
            parameter_values=substance_dict
        )
        if error_msg is not None:
            error_subwindow(self, error_msg)
            return

        self.master.master.refresh_parameters()
        self.master.destroy()

    def fill_content(self):
        self.header = HEADER_TEXT

        self.build_frames()

        self.name_entry = ctk.CTkEntry(
            master=self.content_frame,
            placeholder_text=PARAMNAME_PLACEHOLDER,
            font=STANDARD
        )
        self.name_entry.grid(row=0, column=0, pady=5, padx=20, sticky="ew")

        self.row_frame = ctk.CTkScrollableFrame(
            master=self.content_frame,
            width=400
        )
        self.row_frame.columnconfigure(0, weight=1)
        self.row_frame.grid(row=1, column=0, pady=5, padx=5, sticky="ew")
        self.content_frame.columnconfigure(0, weight=1)
        self.content_frame.columnconfigure(1, weight=1)

        self.list_frame = ListFrame(
            master=self.content_frame,
            width=400
        )
        self.list_frame.grid(row=1, column=1, pady=5, padx=5, sticky="ew")

        self._create_row()
        self._create_row()

        save_button = ctk.CTkButton(
            master=self.bottom_frame,
            text="Save",
            width=20,
            command=lambda: self._command_save_parameter(),
            text_color="black",
            fg_color="light blue"
        )
        save_button.grid(row=0, column=1, pady=5, padx=10)
        add_button = ctk.CTkButton(
            master=self.bottom_frame,
            text="Add row",
            command=lambda: self._create_row(),
            width=10,
            text_color="black",
            fg_color="light blue"
        )
        add_button.grid(row=0, column=0, pady=5, padx=10)

class ListFrame(ctk.CTkScrollableFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.smiles_dict = None

        self._create_smiles_dict()

        self.build_rows()

    def _create_smiles_dict(self):
        smiles: smiles_type = smiles_dict_from_yaml()
        error = verify_entries(smiles)
        if error is not None:
            error_subwindow(self, error)
            return

        self.smiles_dict = smiles

    def _initialize_geometry(self):
        pass

    def _create_row(self, text: str, index: int):
        checkbox = None
        row = ctk.CTkFrame(master=self, fg_color="light grey", width=250)
        row.columnconfigure(0, weight=0)
        row.columnconfigure(1, weight=1)
        label = ctk.CTkLabel(
            master=row,
            text=text,
            font=STANDARD
        )
        if not text == f"--- {text.strip('- ').upper()} ---":
            checkbox = ctk.CTkCheckBox(
                master=row,
                text="",
                fg_color=FGCOLOR,
                text_color=TEXTCOLOR,
                width=16
            )
            row.columnconfigure(0)
            checkbox.grid(row=0, column=0, pady=2, padx=2, sticky="w")
            label.grid(row=0, column=1, pady=2, padx=10, sticky="w")
        else:
            label.grid(row=0, column=0, sticky="ew", pady=2, padx=10, columnspan=2)

        row.grid(row=index, column=0, sticky="ew")

        return checkbox

    def build_rows(self):
        if self.smiles_dict is None:
            return

        index = 0
        checkbox_dict = {}

        for group, molecule in self.smiles_dict.items():
            self._create_row(f"--- {group.upper()} ---", index)
            index += 1
            for name, smiles_string in molecule.items():
                checkbox = self._create_row(f"{name}", index)
                checkbox_dict[name] = checkbox
                index += 1



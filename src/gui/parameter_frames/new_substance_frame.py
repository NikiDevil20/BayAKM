import customtkinter as ctk

from src.bayakm.parameters import write_to_parameters_file
from src.gui.main_gui.gui_constants import STANDARD, FGCOLOR, TEXTCOLOR, ROWFGCOLOR
from src.gui.help import error_subwindow
from src.gui.main_gui.new_page_factory import BaseFrame

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

    def _create_row(self):
        """Creates a row with two entries for substance name and SMILES string.
        Rows can be added and removed via button press.
        """
        row = ctk.CTkFrame(master=self.row_frame, fg_color=ROWFGCOLOR)
        row.grid(
            row=len(self.row_list) + 1, column=0,
            pady=5, padx=10,
            sticky="ew", columnspan=2
        )

        substance_name_entry = ctk.CTkEntry(
            master=row,
            placeholder_text=SUBSTNAME_PLACEHOLDER,
            font=STANDARD
        )
        smiles_entry = ctk.CTkEntry(
            master=row,
            placeholder_text=SMILES_PLACEHOLDER,
            font=STANDARD
        )

        substance_name_entry.grid(row=0, column=0, pady=5, padx=10)
        smiles_entry.grid(row=0, column=1, pady=5, padx=10)

        # Add one remove button per row,
        # which removes it upon click.
        remove_button = ctk.CTkButton(
            master=row,
            text="-",
            command=lambda: row.destroy(),
            width=10,
            fg_color=FGCOLOR,
            text_color=TEXTCOLOR
        )
        remove_button.grid(row=0, column=2, pady=5, padx=10)

        # Row's entries are placed in a list,
        # so their values can be retrieved.
        self.row_list.append((substance_name_entry, smiles_entry))

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
        write_to_parameters_file(
            mode="substance",
            parameter_name=self.name_entry.get(),
            parameter_values=substance_dict
        )

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

        self.row_frame = ctk.CTkScrollableFrame(master=self.content_frame)
        self.row_frame.grid(row=1, column=0, pady=5, padx=5)

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

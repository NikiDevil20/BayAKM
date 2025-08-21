import customtkinter as ctk

from src.bayakm.parameters import write_to_parameters_file
from src.gui.help import error_subwindow
from src.gui.gui_constants import HEADER, STANDARD


class AddSubstanceFrame(ctk.CTkFrame):
    def __init__(self, master=None):
        super().__init__(master)

        self.row_list = []

        # Creating frames
        self._create_header_frame()
        self._create_content_frame()
        self._create_bottom_frame()

    def _create_header_frame(self):
        """Creating the header frame, which contains the header."""
        header_frame = ctk.CTkFrame(master=self, fg_color="light blue")
        header_frame.grid(
            row=0, column=0,
            pady=5, padx=10,
            sticky="ew",
        )
        header = ctk.CTkLabel(
            master=header_frame,
            text="Add substance parameter",
            font=HEADER
        )
        header.pack(pady=10, padx=30)

    def _create_content_frame(self):
        """Scrollable frame, in which the rows for
        substance name and smiles string are placed.
        """
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
            placeholder_text="Parameter name",
            font=STANDARD
        )
        self.name_entry.grid(
            row=0, column=0,
            pady=5, padx=20,
            sticky="ew"
        )

        # Initially creating two rows, because we
        # need at least two values per parameter.
        self._create_row()
        self._create_row()

    def _create_row(self):
        """Creates a row with two entries for substance name and SMILES string.
        Rows can be added and removed via button press.
        """
        row = ctk.CTkFrame(master=self.content_frame)
        row.grid(
            row=len(self.row_list) + 1, column=0,
            pady=5, padx=10,
            sticky="ew", columnspan=2
        )

        substance_name_entry = ctk.CTkEntry(
            master=row,
            placeholder_text="Substance name",
            font=STANDARD
        )
        smiles_entry = ctk.CTkEntry(
            master=row,
            placeholder_text="SMILES string",
            font=STANDARD
        )

        substance_name_entry.grid(
            row=0, column=0,
            pady=5, padx=10
        )
        smiles_entry.grid(
            row=0, column=1,
            pady=5, padx=10
        )

        # Add one remove button per row,
        # which removes it upon click.
        remove_button = ctk.CTkButton(
            master=row,
            text="-",
            command=lambda: row.destroy(),
            width=10,
            fg_color="light blue",
            text_color="black"
        )
        remove_button.grid(
            row=0, column=2,
            pady=5, padx=10
        )

        # Row's entries are placed in a list,
        # so their values can be retrieved.
        self.row_list.append((substance_name_entry, smiles_entry))

    def _create_bottom_frame(self):
        """Creates the bottom frame with save and add button."""
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
            command=lambda: self._command_save_parameter(),
            text_color="black",
            fg_color="light blue"
        )
        save_button.grid(
            row=0, column=1,
            pady=5, padx=10
        )
        add_button = ctk.CTkButton(
            master=bottom_frame,
            text="Add row",
            command=lambda: self._create_row(),
            width=10,
            text_color="black",
            fg_color="light blue"
        )
        add_button.grid(
            row=0, column=0,
            pady=5, padx=10
        )

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

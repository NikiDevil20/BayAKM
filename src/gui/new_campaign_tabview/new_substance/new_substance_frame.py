import customtkinter as ctk

from src.logic.parameters.parameters import write_to_parameters_file
from src.gui.main.gui_constants import (STANDARD, FGCOLOR, TEXTCOLOR,
                                        ROWFGCOLOR, PackagedWidget, Row)
from src.gui.help.help import error_subwindow
from src.gui.new_campaign_tabview.new_page_factory import BaseFrame
from src.logic.smiles.smiles_loader import (smiles_dict_from_yaml, is_valid_smiles)

HEADER_TEXT = "New Substance Parameter"
PARAMNAME_PLACEHOLDER = "Parameter name"
SMILES_PLACEHOLDER = "SMILES"
SUBSTNAME_PLACEHOLDER = "name"


class NewSubstanceParameterFrame(BaseFrame):
    def __init__(self, master):
        super().__init__(master)
        self.subheaeder_frame = None
        self.row_list = []
        self.name_entry = None
        self.row_frame = None
        self.list_frame = None
        self.group_list = []
        self.checked_molecules = []
        self.smiles_list = []
        self.smiles_dict = smiles_dict_from_yaml()
        self.smiles_dict_flattened = self._flatten_smiles_dict()

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
            width=100
        )
        smiles_entry = ctk.CTkEntry(
            master=row,
            placeholder_text=SMILES_PLACEHOLDER,
            font=STANDARD,
            width=100
        )

        substance_name_entry.grid(row=0, column=0, pady=5, padx=10)
        smiles_entry.grid(row=0, column=1, pady=5, padx=10)

        remove_button = ctk.CTkButton(
            master=row,
            text="-",
            command=lambda: self._delete_row(row, (substance_name_entry, smiles_entry)),
            width=10,
            fg_color=FGCOLOR,
            text_color=TEXTCOLOR
        )
        remove_button.grid(row=0, column=2, pady=5, padx=10)

        self.row_list.append((substance_name_entry, smiles_entry))

    def _delete_row(self, row, entry_tuple):
        row.destroy()
        self.row_list.remove(entry_tuple)

    def _flatten_smiles_dict(self):
        return {k: v for inner in self.smiles_dict.values() for k, v in inner.items()}

    def _command_save_parameter(self):
        """Method for saving the parameter's name and values.
        The SMILES string is checked by the BayBE package
        upon parameter generation by the build_parameter_list()
        function in the parameters.py file.
        """
        substance_dict: dict[str, str] = {}

        if self.name_entry.get() == "":
            error_subwindow(
                self,
                message="Parameter name cannot be empty."
            )
            return

        substance_dict = self._fetch_checked_substances()

        for (substance_name_entry, smiles_entry) in self.row_list:
            if substance_name_entry.get() == "" or smiles_entry.get() == "":
                continue
            if not is_valid_smiles(smiles_entry.get()):
                error_subwindow(
                    self,
                    message=(
                        f"Invalid SMILES string for {substance_name_entry.get()}: {smiles_entry.get()}\n"
                        f"Common error include dots at the end or spaces "
                    )
                )
                return
            substance_dict[substance_name_entry.get()] = smiles_entry.get()

        if len(substance_dict.keys()) < 2:
            error_subwindow(
                self,
                message="You must add at least two values to a parameter."
            )
            return

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

    def _fetch_checked_substances(self):
        for group in self.group_list:
            checkboxlist = group.return_checkboxlist()
            for checkbox in checkboxlist:
                if checkbox._variable.get():
                    self.checked_molecules.append(checkbox._text)

        if not len(self.checked_molecules) > 0:
            return {}

        self.checked_molecules.sort()

        return {k: v for k, v in self.smiles_dict_flattened.items() if k in self.checked_molecules}

    def _build_buttons(self):
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

    def _build_labels_and_frames(self):
        self.name_entry = ctk.CTkEntry(
            master=self.content_frame,
            placeholder_text=PARAMNAME_PLACEHOLDER,
            font=STANDARD
        )
        self.name_entry.grid(row=0, column=0, pady=[10, 0], padx=20, sticky="ew")

        self.row_frame = ctk.CTkScrollableFrame(
            master=self.content_frame,
            width=250
        )
        self.row_frame.columnconfigure(0, weight=1)
        self.row_frame.grid(row=2, column=2, pady=10, padx=20, sticky="nsew")

        self.subheaeder_frame = ctk.CTkFrame(
            master=self.row_frame,
            fg_color=FGCOLOR
        )
        self.subheaeder_frame.grid(row=0, column=0, pady=5, padx=5, sticky="ew")

        custom_label = ctk.CTkLabel(
            master=self.subheaeder_frame,
            text="Enter custom",
            font=STANDARD
        )
        custom_label.pack(pady=5, padx=10, anchor="n")

        self.content_frame.columnconfigure(0, weight=1)
        self.content_frame.columnconfigure(1, weight=1)

    def build_smiles_frames(self):
        for index, group in enumerate(self.smiles_dict):
            row = 1
            if index % 2 != 0:
                row += 1
                index = 0
            molecules = list(self.smiles_dict[group].keys())
            smiles_frame = SmilesFramesByGroup(
                master=self.content_frame,
                group_name=group,
                molecules=molecules,
            )
            smiles_frame.grid(
                row=row,
                column=index,
                pady=10,
                padx=20,
                sticky="nsew"
            )
            self.group_list.append(smiles_frame)

    def fill_content(self):
        self.header = HEADER_TEXT

        self.build_frames()
        self._build_buttons()
        self._build_labels_and_frames()

        self._create_row()
        self._create_row()

        self.build_smiles_frames()


class SmilesFramesByGroup(ctk.CTkFrame):
    def __init__(self, master, group_name: str, molecules: list[str], **kwargs):
        super().__init__(master, **kwargs)

        self.group_name = group_name
        self.molecules = molecules
        self.scrollframe = None
        self.title_frame = None
        self.checkbox_list = []

        self._build_title_frame()
        self._build_rows()

    def _build_title_frame(self):
        self.title_frame = ctk.CTkFrame(
            master=self,
            fg_color=FGCOLOR
        )
        self.title_frame.grid(row=0, column=0, pady=10, padx=20, sticky="ew")

        title_label = ctk.CTkLabel(
            master=self.title_frame,
            text=f"{self.group_name}",
            font=STANDARD
        )
        title_label.pack(pady=5, padx=10)

    def _build_rows(self):
        self.scrollframe = ctk.CTkScrollableFrame(
            master=self,
        )
        self.scrollframe.grid(row=1, column=0, pady=10, padx=10, sticky="ew")

        for index, molecule in enumerate(self.molecules):
            object_list = []
            check_var = ctk.BooleanVar(value=False)
            packaged_checkbox = PackagedWidget(
                widget_type=ctk.CTkCheckBox,
                fg_color=FGCOLOR,
                text_color=TEXTCOLOR,
                width=16,
                text=molecule,
                onvalue=True,
                offvalue=False,
                variable=check_var
            )
            object_list.append(packaged_checkbox)
            row = Row(
                master=self.scrollframe,
                object_list=object_list,
                weights=[1]
            )
            row.grid(row=1+index, column=0, sticky="ew")
            self.checkbox_list.append(row.return_widget(0))

    def return_checkboxlist(self):
        return self.checkbox_list

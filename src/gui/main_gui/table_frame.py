import customtkinter as ctk
import pandas as pd
import yaml
import math

from baybe.parameters import SubstanceParameter, NumericalDiscreteParameter, NumericalContinuousParameter

from src.environment_variables.dir_paths import DirPaths
from src.bayakm.output import import_output_to_df, create_output, split_import_df, check_path
from src.gui.help import error_subwindow
from src.gui.main_gui.gui_constants import SUBHEADER, TEXTCOLOR, STANDARD, FGCOLOR


class TableFrame(ctk.CTkFrame):
    def __init__(self, master=None, data=None):
        super().__init__(master)

        self.dirs = DirPaths()
        self.param_dict = None

        if not isinstance(data, pd.DataFrame):
            label = ctk.CTkLabel(
                master=self,
                text="Create a new campaign \n to display table.",
                pady=20, padx=20,
                font=SUBHEADER
            )
            label.pack()
        else:
            self._create_table_from_df(data)
            self._create_bottom_frame()

    def _create_header(
            self,
            categories: list[str] | pd.Index
    ):
        header_frame = ctk.CTkFrame(master=self)
        for col, _ in enumerate(categories):
            header_frame.columnconfigure(col, weight=1)
            headline = ctk.CTkLabel(
                master=header_frame,
                text=categories[col],
                width=100
            )
            headline.grid(row=0, column=col)
        header_frame.grid(
            row=0, column=0,
            pady=5, padx=10,
            sticky="ew"
        )

    def _create_row(
            self,
            content: list[int | float | str],
            color
    ):
        entry_list_per_row = []
        background_frame = ctk.CTkFrame(master=self.content_frame)
        for col, _ in enumerate(content):
            entry = ctk.CTkEntry(
                master=background_frame,
                width=100,
                fg_color=color
            )
            value = content[col]
            if isinstance(value, float):
                value = f"{value:.1f}"
            entry.insert(0, value)
            entry.grid(
                row=0, column=col,
                pady=2, padx=2
            )
            entry_list_per_row.append(entry)
        background_frame.pack()
        return entry_list_per_row

    def _create_table_from_df(self, df):
        self.df = df
        self._create_header(df.columns)

        self.content_frame = ctk.CTkScrollableFrame(master=self, width=105 * len(df.columns))
        self.content_frame.grid(row=1, column=0, pady=5, padx=10, sticky="ew")

        self.columnconfigure(0, weight=1)

        self.full_entry_list = [
            self._create_row(
                content=list(series),
                color="light blue" if i % 2 == 0 else "white"
            )
            for i, series in enumerate(df.itertuples(index=False))
        ]

    def _build_param_name_and_value_list(self):
        try:
            with open(self.dirs.return_file_path("parameters"), "r") as f:
                yaml_dict = yaml.safe_load(f)
        except FileNotFoundError:
            print(f"No file found at {self.dirs.return_file_path('parameters')}")

        self.all_params_dict = {}

        if "Numerical Discrete Parameters" in yaml_dict.keys():
            numerical_dict = self._build_numerical_values(yaml_dict)
            self.all_params_dict.update(numerical_dict)
        if "Substance Parameters" in yaml_dict.keys():
            substance_dict = self._build_substance_values(yaml_dict)
            self.all_params_dict.update(substance_dict)
        if "Numerical Continuous Parameters" in yaml_dict.keys():
            continuous_dict = self._build_continuous_values(yaml_dict)
            self.all_params_dict.update(continuous_dict)

    @staticmethod
    def _build_numerical_values(yaml_dict) -> dict[str, list[float]]:
        # numerical_dict = yaml_dict["Numerical Discrete Parameters"]
        # numerical_list = [(key, numerical_dict[key]) for key in numerical_dict.keys()]
        # return numerical_list
        numerical_dict = yaml_dict["Numerical Discrete Parameters"]
        return numerical_dict

    @staticmethod
    def _build_substance_values(yaml_dict) -> dict[str, list[str]]:
        substance_dict = yaml_dict["Substance Parameters"]
        # substance_list = [(key, substance_dict[key].keys()) for key in substance_dict.keys()]
        # for key in substance_dict.keys():
        #     substance_list.append(
        #         (key, substance_dict[key].keys())
        #     )
        return substance_dict

    @staticmethod
    def _build_continuous_values(yaml_dict) -> dict[str, tuple[int, int]]:
        conti_dict = yaml_dict["Numerical Continuous Parameters"]
        # conti_list = [(key, conti_dict[key]) for key in conti_dict.keys()]
        return conti_dict

    def _read_table(self):
        # self._build_param_name_and_value_list()
        rows = []
        columns = self.df.columns
        error_list = []

        for row_index, row_list in enumerate(self.full_entry_list):
            row = []
            for column_index, entry in enumerate(row_list):
                value, error = self._validate_entry(
                    entry.get(),
                    columns[column_index],
                    row_index
                )
                if error:
                    error_list.append(error)
                row.append(value)
            rows.append(row)

        if error_list:
            for error in error_list:
                error_subwindow(self, error)
            return

        df = pd.DataFrame(rows, columns=columns)
        create_output(df)
        self.master.refresh_content()

    def _validate_entry(self, value, column, row_index):
        # Validierung und Typkonvertierung je nach Spalte
        self.param_dict = self.master.campaign.get_param_dict()
        try:
            if column == "Yield":
                value = float(value)
                if not 0 <= value <= 100 and not math.isnan(value):
                    return value, f"Yield '{value}' in row {row_index + 1} must be between 0 and 100."

            elif column != "Journal number":
                for param_class in self.param_dict.keys():
                    for parameter in self.param_dict[param_class]:

                        if column == parameter.name:
                            current_parameter = parameter

                            if isinstance(current_parameter, (SubstanceParameter, NumericalDiscreteParameter)):
                                allowed_values = current_parameter.values

                                if isinstance(current_parameter, NumericalDiscreteParameter):
                                    # try:
                                    value = float(value)
                                    # except ValueError:
                                    #     return value, f"Value '{value}' in column {column} must be a number."

                                if value not in allowed_values:
                                    return value, f"Value '{value}' in column {column} is not allowed. Allowed values: {allowed_values}"

                            elif isinstance(current_parameter, NumericalContinuousParameter):
                                lower = current_parameter.bounds.lower
                                upper = current_parameter.bounds.upper

                                if not (lower <= float(value) <= upper):
                                    return value, f"Value '{value}' in column {column} must be between {lower} and {upper}."

            return value, None
        except ValueError:
            return value, f"Entered value: {value} in column {column} is of invalid type."

    def _create_bottom_frame(self):
        self.bottom_frame = ctk.CTkFrame(master=self)
        self.bottom_frame.grid(
            row=3, column=0,
            pady=5, padx=10,
            sticky="ew"
        )

        save_button = ctk.CTkButton(
            master=self.bottom_frame,
            text="Save",
            command=lambda: self._read_table(),
            text_color=TEXTCOLOR,
            font=STANDARD,
            fg_color=FGCOLOR
        )
        save_button.grid(row=0, column=0, pady=5, padx=10, sticky="ew")
        new_reco_button = ctk.CTkButton(
            master=self.bottom_frame,
            text="New recommendation",
            command=lambda: self._get_new_recommendation(),
            text_color=TEXTCOLOR,
            font=STANDARD,
            fg_color=FGCOLOR
        )
        new_reco_button.grid(row=0, column=1, pady=5, padx=10, sticky="ew")

    def _get_new_recommendation(self):
        self._read_table()

        if check_path(self.dirs.return_file_path("output")):
            full_input: pd.DataFrame = import_output_to_df()
            measurements, pending = split_import_df(full_input)
            if measurements.empty:
                measurements = None
            if pending.empty:
                pending = None
        else:
            measurements, pending = None, None
        self.master.campaign.get_recommendation(
            initial=False,
            measurements=measurements,
            pending=pending
        )
        self.master.campaign.save_campaign()
        self.master.refresh_content()


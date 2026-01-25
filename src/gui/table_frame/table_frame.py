import customtkinter as ctk
import pandas as pd
import yaml
import math
import numpy as np

from baybe.parameters import SubstanceParameter, NumericalDiscreteParameter, NumericalContinuousParameter
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from src.logic.config.config_loader import Config
from src.environment.dir_paths import DirPaths
from src.logic.output.output import import_output_to_df, create_output, split_import_df, check_path
from src.gui.help.help import error_subwindow
from src.gui.table_frame.YieldPlotter import YieldPlotter
from src.gui.main.gui_constants import SUBHEADER, TEXTCOLOR, STANDARD, FGCOLOR
from src.logic.parameters.parameters import build_param_list


class TableFrame(ctk.CTkFrame):
    def __init__(self, master=None, data=None):
        super().__init__(master)

        self.dirs = DirPaths()

        self.categories = None

        if not isinstance(data, pd.DataFrame):
            label = ctk.CTkLabel(
                master=self,
                text="Create a new campaign \n to display table.",
                pady=20, padx=20,
                font=SUBHEADER
            )
            label.pack()
        else:
            self.param_dict = self.master.campaign.get_param_dict()
            self._create_table_from_df(data)
            self._create_bottom_frame()
            self.build_plot_frame()

    def _create_header(
            self,
            categories: list[str] | pd.Index,
            parameter_dict: dict[str, list[str]]
    ):
        header_frame = ctk.CTkFrame(master=self)
        width = 120
        length_dict = {}
        print(parameter_dict)
        for param in parameter_dict.keys():
            length = len(max(parameter_dict[param], key=len))
            length_dict[param] = length
            print(param, length)

        for col, _ in enumerate(categories):
            match categories[col]:
                case "Journal no.":
                    width = 60
                case "Batch":
                    width = 50
                case "Yield":
                    width = 50
                case _:
                    width = length_dict[categories[col]] * 11
                    print(width)

            header_frame.columnconfigure(col, weight=1)
            headline = ctk.CTkLabel(
                master=header_frame,
                text=categories[col],
                width=width
            )
            headline.grid(row=0, column=col, padx=10)
        header_frame.grid(
            row=0, column=0,
            pady=5, padx=5,
            sticky="ew"
        )

    @staticmethod
    def _param_dict_from_list(parameter_list) -> dict[str, list[str]]:
        param_dict = {}
        print(parameter_list)
        for param in parameter_list:
            if isinstance(param, NumericalDiscreteParameter):
                param_dict[param.name] = [str(v) for v in param.values]
            else:
                param_dict[param.name] = [str(v) for v in param.data.keys()]
        return param_dict

    def _create_table_from_df(self, df):
        self.df = df
        self.categories: list[str] = df.columns
        parameter_list = build_param_list()
        param_dict = self._param_dict_from_list(parameter_list)
        self._create_header(df.columns, param_dict)
        self.all_valid_entries = []
        self.batch_no_list = list(df["Batch"])

        for parameter_name in self.categories:
            if parameter_name in ["Journal no.", "Yield"]:
                self.all_valid_entries.append(None)
            valid_entries = self._get_vaild_entries_per_column(parameter_name)
            self.all_valid_entries.append(valid_entries)

        self.content_frame = ctk.CTkScrollableFrame(
            master=self,
            # width=125 * len(df.columns)
        )
        self.content_frame.grid(row=1, column=0, pady=[0, 5], padx=10, sticky="nsew")

        self.columnconfigure(0, weight=1)

        self.row_list_list = [
            Row(
                master=self.content_frame,
                col_content=self.all_valid_entries,
                row_content=list(series),
                color="light blue" if i % 2 == 0 else "white",
                batch_no=self.batch_no_list[i]
            )
            for i, series in enumerate(df.itertuples(index=False))
        ]
        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=1)

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

        for row_index, row_object in enumerate(self.row_list_list):
            row = []
            for column_index, entry in enumerate(row_object.entry_list):
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
        try:
            if column == "Yield":
                if value == "":
                    value = 0.00
                value = float(value)
                if not 0 <= value <= 100 and not math.isnan(value):
                    return value, f"Yield '{value}' in row {row_index + 1} must be between 0 and 100."

            elif column != "Journal no.":
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
            pady=[0, 5], padx=10,
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
        save_button.grid(row=0, column=1, pady=5, padx=10, sticky="ew")
        new_reco_button = ctk.CTkButton(
            master=self.bottom_frame,
            text="New recommendation",
            command=lambda: self._get_new_recommendation(),
            text_color=TEXTCOLOR,
            font=STANDARD,
            fg_color=FGCOLOR
        )
        new_reco_button.grid(row=0, column=2, pady=5, padx=10, sticky="ew")

        add_row_button = ctk.CTkButton(
            master=self.bottom_frame,
            text="Add row",
            command=lambda: self._add_empty_row(),
            text_color=TEXTCOLOR,
            font=STANDARD,
            fg_color=FGCOLOR
        )
        add_row_button.grid(row=0, column=0, pady=5, padx=10, sticky="ew")

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
            pending=pending,
            full_input_with_yield=measurements
        )
        self.master.campaign.save_campaign()
        self.master.refresh_content()

    def _get_vaild_entries_per_column(self, column_name: str) -> list[str]:
        for parameter_category in self.param_dict.keys():
            for parameter in self.param_dict[parameter_category]:
                if parameter.name == column_name:
                    if isinstance(parameter, SubstanceParameter):
                        return list(parameter.data.keys())
                    elif isinstance(parameter, NumericalDiscreteParameter):
                        return list(parameter.values)
                    else:
                        TypeError("Parameter Type not supported")
                        return []
                continue
        return []

    def _add_empty_row(self):
        cfg = Config()
        i = len(self.row_list_list)
        n = len(self.df.columns)
        journal_prefix = cfg.dict["Journal prefix"]
        batch_no = str(max(self.batch_no_list))
        color = "light blue" if i % 2 == 0 else "white"
        row_content = []

        for x in range(n-3):
            row_content.append("")
        row_content.append(journal_prefix)
        row_content.append(batch_no)
        row_content.append("")
        self.row_list_list.append(
            Row(
                master=self.content_frame,
                col_content=self.all_valid_entries,
                row_content=row_content,
                color=color,
                batch_no=batch_no
            )
        )

    def build_plot_frame(self):
        if self._number_of_batches() < 2:
            return

        yield_list = list(self.df["Yield"])
        batch_no_list = self.batch_no_list
        data: list[list[float]] = []

        for n in range(self._number_of_batches()):
            data.append([])

        for index, batch_no in enumerate(batch_no_list):
            data[batch_no-1].append(yield_list[index])

        for v_list in data:
            empty_allowed = 0
            for value in v_list:
                if value == "":
                    empty_allowed += 1
            if empty_allowed == len(v_list):
                return

        plot_frame = PlotFrame(master=self, data=data)
        plot_frame.grid(row=0, column=2, pady=5, padx=10, rowspan=3)

    def _number_of_batches(self):
        unique_batches = set(self.batch_no_list)
        return len(unique_batches)




class Row:
    def __init__(
            self,
            col_content: list[int | float | str],
            row_content: list[list[int | float | str]],
            color,
            master=None,
            batch_no="1"
    ):
        self.master = master
        self.col_content = col_content
        self.row_content = row_content
        self.color = color
        self.batch_no = batch_no

        self.state = "readonly"

        self.entry_list = self._create_widgets()

        if self.row_complete():
            self.disable_row()

    def _batch_no_entry(self, master):

        entry = ctk.CTkEntry(
            width=10,
            master=master
        )
        entry.grid(row=0, column=0, pady=2, padx=2)
        entry.insert(0, self.batch_no)
        return entry

    def _create_widgets(self):
        entry_list_per_row = []
        background_frame = ctk.CTkFrame(master=self.master)

        self.batch_widget = self._batch_no_entry(master=background_frame)

        for col_number in range(len(self.row_content) - 3):
            combo_box = self._create_combobox(
                master=background_frame,
                starting_value=self.row_content[col_number],  # Type: ignore
                all_values=self.col_content[col_number],  # Type: ignore
                color=self.color,
                position=col_number
            )
            entry_list_per_row.append(combo_box)
            background_frame.columnconfigure(col_number, weight=1)
        for col_number in [3, 2, 1]:
            index = len(self.row_content) - col_number
            width = 60
            if col_number == 2:
                width = 30
            entry = ctk.CTkEntry(
                fg_color=self.color,
                master=background_frame,
                width=width
            )
            entry.insert(0, _format_to_str(self.row_content[index], is_yield=True))  # Type: ignore
            entry.grid(row=0, column=index, pady=2, padx=2, sticky="ew")
            background_frame.columnconfigure(index, weight=1)
            entry_list_per_row.append(entry)
        background_frame.pack(expand=True, fill="both")
        return entry_list_per_row

    @staticmethod
    def _create_combobox(
            master,
            starting_value: int | str | float,
            all_values: list[int | str | float],
            color: str,
            position: int
    ) -> ctk.CTkComboBox:
        starting_value = _format_to_str(starting_value)
        all_values = [_format_to_str(v) for v in all_values]
        string_length = len(max(all_values, key=len))
        width = string_length * 8 + 40

        combo_box = ctk.CTkComboBox(
            master=master,
            fg_color=color,
            values=all_values,
            width=width,
            state="readonly",
            text_color_disabled="black"
        )
        combo_box.set(starting_value)
        combo_box.grid(row=0, column=position, pady=2, padx=2, sticky="ew")
        return combo_box

    def disable_row(self):
        if self.state == "disabled":
            return
        for widget in self.entry_list:
            try:
                widget.configure(state="disabled")
            except Exception:
                pass
        self.state = "disabled"

    def enable_row(self):
        if self.state == "readonly":
            return
        for widget in self.entry_list:
            try:
                widget.configure(state="readonly")
            except Exception:
                widget.configure(state="normal")
        self.state = "readonly"

    def toggle_row(self):
        if self.state == "normal":
            self.disable_row()
        else:
            self.enable_row()

    def _has_yield(self) -> bool:
        try:
            yield_entry: str = self.entry_list[-1].get()
            return yield_entry.strip() != ""
        except Exception:
            return False

    def _has_journal(self) -> bool:
        try:
            journal_number: str = self.entry_list[-3].get()
            return bool(journal_number and journal_number[-1].isdigit())
        except Exception:
            return False

    def row_complete(self) -> bool:
        return self._has_journal() and self._has_yield()

    def batch_number(self):
        return self.batch_widget.get()


class PlotFrame(ctk.CTkFrame):
    def __init__(self, master=None, data=None):
        super().__init__(master)
        self.data = data

        self._build_plot()

    def _build_plot(self):
        plotter = YieldPlotter(self.data)
        fig, ax = plotter.create_plot()

        canvas = FigureCanvasTkAgg(fig, master=self)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)


def _format_to_str(value: float | int, is_yield: bool = False) -> str:
    try:
        value = np.nan_to_num(value)
        return str(value)
    except Exception:
        if is_yield and isinstance(value, float):
            return str(int(value))
        if isinstance(value, float):
            return f"{value:.1f}"
        return str(value)


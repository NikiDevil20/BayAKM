import customtkinter as ctk
import pandas as pd
from gpytorch.beta_features import checkpoint_kernel

from src.bayakm.output import import_output_to_df, create_output, split_import_df, check_path
from src.bayakm.dir_paths import DirPaths


class TableFrame(ctk.CTkFrame):
    def __init__(self, master=None, data=None):
        super().__init__(master)

        self.dirs = DirPaths()
        if not isinstance(data, pd.DataFrame):
            label = ctk.CTkLabel(
                master=self,
                text="Create a new campaign \n to display table.",
                pady=5, padx=5, corner_radius=15
            )
            label.pack()
        else:
            self._create_table_from_df(data)
            self._create_bottom_frame()

    def _create_header(self, categories: list[str] | pd.Index):
        header_frame = ctk.CTkFrame(master=self)
        for col, _ in enumerate(categories):
            header_frame.columnconfigure(col, weight=1)
            headline = ctk.CTkLabel(master=header_frame, text=categories[col], width=100)
            headline.grid(row=0, column=col)
        header_frame.grid(row=0, column=0, pady=5, padx=10)

    def _create_row(self, content: list[int | float | str]):
        entry_list_per_row = []
        background_frame = ctk.CTkFrame(master=self.content_frame)
        for col, _ in enumerate(content):
            entry = ctk.CTkEntry(master=background_frame, width=100,)
            entry.insert(0, content[col])
            entry.grid(row=0, column=col, pady=2, padx=2)
            entry_list_per_row.append(entry)
        background_frame.pack()
        return entry_list_per_row

    def _create_table_from_df(self, df):
        self.df = df
        self._create_header(df.columns)
        self.full_entry_list = []
        self.content_frame = ctk.CTkFrame(master=self)
        self.content_frame.grid(row=1, column=0, pady=5, padx=10)
        for series in df.itertuples(index=False):
            entry_list_per_row = self._create_row(content=list(series))
            self.full_entry_list.append(entry_list_per_row)

    def _read_table(self):
        rows = []
        for row_list in self.full_entry_list:
            row_values = [entry.get() for entry in row_list]
            rows.append(row_values)
        columns = self.df.columns
        df = pd.DataFrame(rows, columns=columns)
        create_output(df)
        self.master.refresh_content()


    def _create_bottom_frame(self):
        self.bottom_frame = ctk.CTkFrame(master=self)
        self.bottom_frame.grid(row=3, column=0, pady=5, padx=10)

        save_button = ctk.CTkButton(
            master=self.bottom_frame,
            text="Save",
            command=lambda: self._read_table()
        )
        save_button.grid(row=0, column=0, pady=5, padx=10)
        new_reco_button = ctk.CTkButton(
            master=self.bottom_frame,
            text="New recommendation",
            command=lambda: self._get_new_recommendation()
        )
        new_reco_button.grid(row=0, column=1, pady=5, padx=10)

    def _get_new_recommendation(self):
        self._read_table()
        if check_path(self.dirs.output_path):
            full_input: pd.DataFrame = import_output_to_df()
            measurements, pending = split_import_df(full_input)
        else:
            measurements, pending = None, None
        self.master.campaign.get_recommendation(
            initial=False,
            measurements=measurements,
            pending=pending
        )
        self.master.campaign.save_campaign()
        self.master.refresh_content()




import customtkinter as ctk
import pandas as pd

from src.bayakm.dir_paths import DirPaths
from src.bayakm.output import import_output_to_df, create_output, split_import_df, check_path
from src.gui.gui_constants import SUBHEADER


class TableFrame(ctk.CTkFrame):
    def __init__(self, master=None, data=None):
        super().__init__(master)

        self.dirs = DirPaths()

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
            entry.insert(0, content[col])
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

    def _read_table(self):
        rows = [[entry.get() for entry in row_list] for row_list in self.full_entry_list]
        columns = self.df.columns
        df = pd.DataFrame(rows, columns=columns)
        create_output(df)
        self.master.refresh_content()

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
            command=lambda: self._read_table()
        )
        save_button.grid(
            row=0, column=0,
            pady=5, padx=10
        )
        new_reco_button = ctk.CTkButton(
            master=self.bottom_frame,
            text="New recommendation",
            command=lambda: self._get_new_recommendation()
        )
        new_reco_button.grid(
            row=0, column=1,
            pady=5, padx=10
        )

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




import customtkinter as ctk
import pandas as pd

from src.bayakm.output import import_output_to_df


class TableFrame(ctk.CTkFrame):
    def __init__(self, master=None, content=None):
        super().__init__(master)

        if not content:
            label = ctk.CTkLabel(
                master=self,
                text="Create a new campaign \n to display table.",
                pady=5, padx=5, corner_radius=15
            )
            label.pack()
        else:
            self._create_table_from_df(content)

    def _create_header(self, categories: list[str] | pd.Index):
        header_frame = ctk.CTkFrame(
            master=self
        )
        header_frame.rowconfigure(0, weight=1)
        for col in range(len(categories)):
            header_frame.columnconfigure(col, weight=1)
            headline = ctk.CTkLabel(
                master=header_frame,
                text=categories[col],
                width=100
            )
            headline.grid(row=0, column=col)
        header_frame.pack()

    def _create_row(self, content: list[int | float | str]):
        background_frame = ctk.CTkFrame(master=self)
        background_frame.rowconfigure(0, weight=1)
        for col in range(len(content)):
            background_frame.columnconfigure(col, weight=1)
            entry = ctk.CTkEntry(master=background_frame, width=100,)
            entry.insert(0, content[col])
            entry.grid(row=0, column=col)
        background_frame.pack()

    def _create_table_from_df(self, df):
        self._create_header(df.columns)
        for series in df.itertuples(index=False):
            self._create_row(content=list(series))
        self.table_state = True

    def _read_row(self) -> pd.Series:
        row = pd.Series()
        return row

    def _save_changes_to_df(self) -> pd.DataFrame:
        df = pd.DataFrame()
        return df







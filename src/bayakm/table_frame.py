import customtkinter as ctk
import pandas as pd


class TableFrame(ctk.CTkFrame):
    def __init__(self, master=None):
        super().__init__(master)

        self.table_state = False
        if not self.table_state:
            label = ctk.CTkLabel(master=self, text="No table to display.", pady=5, padx=5)
            label.pack()

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

    def _create_row(self, content: list[int | float | str] | pd.Series):
        background_frame = ctk.CTkFrame(master=self)
        background_frame.rowconfigure(0, weight=1)
        for col in range(len(content)):
            background_frame.columnconfigure(col, weight=1)
            entry = ctk.CTkEntry(master=background_frame, width=100,)
            entry.insert(0, content[col])
            entry.grid(row=0, column=col)
        background_frame.pack()

    def create_table_from_df(self, df: pd.DataFrame):
        self._create_header(df.columns)
        for series in df.itertuples(index=False):
            print(series)
            self._create_row(content=list(series))
        self.table_state = True





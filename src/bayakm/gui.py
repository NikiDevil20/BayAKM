import customtkinter as ctk
import pandas as pd

from src.bayakm.main_frame import MainFrame
from src.bayakm.table_frame import TableFrame
ctk.set_default_color_theme("dark-blue")


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.tableframe = None
        self.main_frame = None

        for row in range(3):
            self.rowconfigure(row, weight=1)
        for col in range(3):
            self.columnconfigure(col, weight=1)

        self._initialize_geometry()
        self._create_header()
        self._display_recommendation()
        self._create_main_frame()
        self._create_info_frame()

    def _initialize_geometry(self):
        self.title("BayAKM")
        # self.geometry("400x400")

    def _create_header(self):
        self.header_frame = ctk.CTkFrame(master=self)
        self.header_frame.configure(
            fg_color="light blue"
        )
        header = ctk.CTkLabel(
            master=self.header_frame,
            text="Dies ist ein Titel.",
            font=("Arial", 24),
        )
        header.pack(pady=20, padx=40)
        self.header_frame.grid(row=0, column=0, columnspan=3, pady=10, padx=10, sticky="ew")

    def _create_main_frame(self):
        self.main_frame = MainFrame(master=self)
        self.main_frame.grid(row=1, column=0, pady=5, padx=10)

    def _display_recommendation(self):
        self.tableframe = TableFrame(master=self)
        # self.tableframe.create_table_from_df()
        self.tableframe.grid(row=1, column=1, pady=5, padx=10)

    def _create_info_frame(self):
        self.info_frame = ctk.CTkFrame(master=self)
        label = ctk.CTkLabel(
            master=self.info_frame,
            text="Hier könnte ein Infotext stehen.")
        label.pack(padx=5, pady=5)
        self.info_frame.grid(row=2, column=0, columnspan=3, pady=5, padx=10, sticky="ew")



def main():

    app = App()
    app.mainloop()


if __name__ == "__main__":
    main()

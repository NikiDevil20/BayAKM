import customtkinter as ctk
from src.gui.menu_frame import MenuFrame
from src.gui.table_frame import TableFrame
from src.bayakm.output import check_path, import_output_to_df
from src.bayakm.dir_paths import DirPaths
from src.bayakm.bayakm_campaign import BayAKMCampaign
from src.bayakm.parameters import build_param_list
from src.bayakm.probability_of_improvement import print_pi
from src.bayakm.config_loader import Config
# ctk.set_default_color_theme("dark-blue")


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.table_frame = None
        self.menu_frame = None
        self.dirs = DirPaths()
        self.cfg = Config()
        self.campaign = None

        self._initialize_geometry()
        self._initialize_campaign()
        self._create_header()
        self._display_recommendation()
        self._create_menu_frame()
        self._create_info_frame()

    def _initialize_geometry(self):
        self.title("BayAKM")

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

    def _create_menu_frame(self):
        self.menu_frame = MenuFrame(master=self)
        self.menu_frame.grid(row=1, column=0, pady=5, padx=10)

    def _display_recommendation(self):
        if check_path(self.dirs.output_path):
            data = import_output_to_df()
        else:
            data = None

        self.table_frame = TableFrame(master=self, data=data)
        self.table_frame.grid(row=1, column=1, pady=5, padx=10)

    def _create_info_frame(self):
        self.info_frame = ctk.CTkFrame(master=self)
        label = ctk.CTkLabel(
            master=self.info_frame,
            text="Hier könnte ein Infotext stehen.")
        label.pack(padx=5, pady=5)
        self.info_frame.grid(row=2, column=0, columnspan=3, pady=5, padx=10, sticky="ew")

    def refresh_content(self):
        self.menu_frame.destroy()
        self._create_menu_frame()
        self.table_frame.destroy()
        self._display_recommendation()

    def _initialize_campaign(self):
        if check_path(self.dirs.param_path):
            self.parameter_list = build_param_list()
            if check_path(self.dirs.campaign_path):
                self.campaign = BayAKMCampaign(self.parameter_list)
                if self.cfg.pi:
                    self.campaign.attach_hook([print_pi])




def main():
    app = App()
    app.mainloop()


if __name__ == "__main__":
    main()

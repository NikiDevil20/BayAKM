import customtkinter as ctk

from src.bayakm.bayakm_campaign import BayAKMCampaign
from src.bayakm.config_loader import Config
from src.environment_variables.dir_paths import DirPaths
from src.bayakm.output import check_path, import_output_to_df
from src.bayakm.parameters import build_param_list
from src.gui.main_gui.gui_constants import HEADER, STANDARD
from src.gui.main_gui.menu_frame import MenuFrame
from src.gui.main_gui.table_frame import TableFrame


# ctk.set_default_color_theme("dark-blue")


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.table_frame = None
        self.menu_frame = None
        self.campaign = None
        self.parameter_list = None
        self.dirs = DirPaths()
        self.cfg = Config()

        # Initializing content
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
            text="BayAKM",
            font=HEADER,
        )
        header.grid(
            row=0, column=0,
            pady=20, padx=50,
            sticky="w"
        )
        subheader = ctk.CTkLabel(
            master=self.header_frame,
            text="A convenient gui based tool for bayesian reaction optimization",
            font=STANDARD
        )
        subheader.grid(
            row=0, column=1,
            pady=5, padx=40,
            sticky="w"
        )
        self.header_frame.grid(
            row=0, column=0,
            pady=10, padx=10,
            sticky="ew", columnspan=3
        )

    def _create_menu_frame(self):
        self.menu_frame = MenuFrame(master=self)
        self.menu_frame.grid(
            row=1, column=0,
            pady=5, padx=10,
            sticky="nw"
        )

    def _display_recommendation(self):
        data = None
        if check_path(self.dirs.environ):
            if check_path(self.dirs.return_file_path("output")):
                data = import_output_to_df()

        # TableFrame is always constructed, but if no real data
        # can be displayed, a message is shown.
        self.table_frame = TableFrame(master=self, data=data)
        self.table_frame.grid(
            row=1, column=1,
            pady=5, padx=10
        )

    def _create_info_frame(self):
        self.info_frame = ctk.CTkFrame(master=self)
        self.info_frame.grid(
            row=2, column=0,
            pady=5, padx=10,
            sticky="ew", columnspan=3
        )

        # Placeholder
        label = ctk.CTkLabel(
            master=self.info_frame,
            text="Hier könnte ein Infotext stehen.")
        label.pack(padx=5, pady=5)

    def refresh_content(self):
        """
        Refresh the content of the GUI, e.g. after a new recommendation
        has been generated.
        """
        self.menu_frame.destroy()
        self._create_menu_frame()

        self.table_frame.destroy()
        self._display_recommendation()

    def _initialize_campaign(self):

        if check_path(self.dirs.environ):
            self.campaign = BayAKMCampaign()
            self.parameter_list = self.campaign.get_parameter_list()
            # if self.cfg.dict["pi"]:
            #     self.campaign.attach_hook([print_pi])  # TODO

    def command_save_campaign_and_get_first_recommendation(self):
        self.campaign = BayAKMCampaign()
        self.campaign.get_recommendation(initial=True)
        self.campaign.save_campaign()
        self.parameter_list = self.campaign.get_parameter_list()
        self.refresh_content()



def main():
    app = App()
    app.mainloop()


if __name__ == "__main__":
    main()

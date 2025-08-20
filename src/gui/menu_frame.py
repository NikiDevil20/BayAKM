import customtkinter as ctk
import pandas as pd

from help import HelpFrame
from param_view_frame import ParamViewFrame
from src.bayakm.bayakm_campaign import BayAKMCampaign
from src.bayakm.config_loader import Config
from src.bayakm.dir_paths import DirPaths
from src.bayakm.output import check_path, import_output_to_df
from src.bayakm.parameters import build_param_list
from src.bayakm.probability_of_improvement import print_pi
from src.gui.new_campaign_tabview import NewCampaignTabview


class MenuFrame(ctk.CTkFrame):
    def __init__(self, master=None, *args, **kwargs):
        super().__init__(master)

        self.dirs = DirPaths()
        self.cfg = Config()
        self.campaign = None

        self.params_list = build_param_list()
        if check_path(self.dirs.campaign_path):
            self._initialize_campaign(self.params_list)

        self._create_subwindows()

    def _create_subwindows(self):
        btn_config = (
            {"name": "New campaign", "parameter_list": self.params_list},
            {"name": "View parameters", "parameter_list": self.params_list},
            {"name": "Help"}
        )
        for i, arguments in enumerate(btn_config):
            button = ctk.CTkButton(
                master=self,
                text=arguments["name"],
                command=lambda args=arguments: self._commands_subwindow(**args),
                font=("Arial", 18),
                text_color="black",
                height=40,
                width=200,
                fg_color="light blue"
            )
            button.grid(row=i+1, column=0, pady=5, padx=10)

    def _commands_subwindow(self, name: str, **kwargs):
        match name:
            case "Help":
                frame_class = HelpFrame
            case "New campaign":
                frame_class = NewCampaignTabview
            case "View parameters":
                frame_class = ParamViewFrame
            case _:
                raise ValueError("Tippfehler?")
        subwindow = ctk.CTkToplevel(self)
        subwindow.title(name)
        subwindow.grab_set()
        subwindow.focus_set()
        subwindow.columnconfigure(0, weight=1)
        subwindow.rowconfigure(0, weight=1)
        subwindow.frame = frame_class(master=subwindow, **kwargs)
        subwindow.frame.grid(row=0, column=0, sticky="nsew")

    def _get_new_recommendation(self):
        print("test")

    def _initialize_campaign(self, parameter_list):
        campaign = BayAKMCampaign(parameter_list)
        if self.cfg.pi:
            campaign.attach_hook([print_pi])
        self.campaign = campaign

def test_func():
    print("Test.")



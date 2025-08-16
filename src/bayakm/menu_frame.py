import customtkinter as ctk
from time import time
from help_frame import HelpFrame
from new_campaign_frame import NewCampaignFrame
from param_view_frame import ParamViewFrame
from src.bayakm.parameters import build_param_list


class MenuFrame(ctk.CTkFrame):
    def __init__(self, master=None, *args, **kwargs):
        super().__init__(master)

        for row in range(3):
            self.rowconfigure(row, weight=0)
        for column in range(3):
            self.columnconfigure(column, weight=0)

        # self.configure(
        #     fg_color="grey",
        #     corner_radius=10,
        # )
        self.params_list = build_param_list()
        self._create_subwindows()

    def _create_subwindows(self):
        btn_config = (
            {"name": "New campaign"},
            {"name": "View parameters", "params": self.params_list},
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
            button.grid(row=i, column=0, pady=5, padx=10)

    def _commands_subwindow(self, name: str, **kwargs):
        match name:
            case "Help":
                frame_class = HelpFrame
            case "New campaign":
                frame_class = NewCampaignFrame
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

def test_func():
    print("Test.")



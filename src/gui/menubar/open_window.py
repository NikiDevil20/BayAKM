from typing import Callable
import customtkinter as ctk

from src.gui.choose_campaign.campaign_manager import CampaignManager
from src.gui.get_insights.insights_frame import InsightsFrame
from src.gui.help.help import HelpFrame
from src.gui.new_campaign_tabview.new_campaign_tabview import NewCampaignTabview
from src.gui.view_parameters.param_view_frame import ParamViewFrame


def open_window(
        master,
        name: str,
        **kwargs
) -> Callable:

    def frame_factory():
        match name:
            case "Help":
                frame_class = HelpFrame
            case "New campaign":
                frame_class = NewCampaignTabview
            case "View parameters":
                frame_class = ParamViewFrame
            case "Get insights":
                frame_class = InsightsFrame
            case "Choose campaign":
                frame_class = CampaignManager
            case _:
                raise ValueError("Tippfehler?")

        subwindow = ctk.CTkToplevel(master)
        subwindow.title(name)
        subwindow.grab_set()
        subwindow.focus_set()
        subwindow.frame = frame_class(
            master=subwindow,
            **kwargs
        )
        if subwindow.frame is not None and hasattr(subwindow.frame, 'winfo_exists') and subwindow.frame.winfo_exists():
            subwindow.frame.grid(row=0, column=0, sticky="nsew")
        else:
            subwindow.destroy()

    return frame_factory

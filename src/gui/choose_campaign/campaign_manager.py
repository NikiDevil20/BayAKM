import os
import shutil
from functools import partial

import customtkinter as ctk

from src.environment.dir_paths import DirPaths
from src.gui.help.help import error_subwindow
from src.gui.gui_constants import Row, PackagedWidget, SUBHEADER, FGCOLOR
from src.gui.new_page_factory import BaseFrame

HEADER_TEXT = "Choose campaign"


class CampaignManager(BaseFrame):
    def __init__(self, master):
        super().__init__(master)

        self.cmp = CampaignHandler()
        self.fill_content()

        self.listframe = None

    def fill_content(self):
        self.header = HEADER_TEXT
        self.build_frames()

        folder_list = self.cmp.build_campaign_list()

        if not folder_list:
            error_msg = "Start a campaign first before switching."
            error_label = ctk.CTkLabel(
                text=error_msg,
                font=SUBHEADER,
                master=self.content_frame
            )
            error_label.pack()
        else:
            listframe = ListFrame(self.content_frame, self.cmp, folder_list)
            listframe.pack()

        bottom_text = ctk.CTkLabel(
            master=self.bottom_frame,
            text=(
                "Switch or delete campaign.\n"
                "Be careful: Removing cannot be undone!"
            )
        )
        bottom_text.pack()


class ListFrame(ctk.CTkScrollableFrame):
    def __init__(self, master, cmp, folder_list):
        super().__init__(master)

        self.cmp = cmp
        self.dirs = DirPaths()
        self.folder_list = folder_list
        self.row_list = []

        self._build_list()

    def _build_list(self):
        self.folder_list = self.cmp.build_campaign_list()
        active_campaign: str = self.dirs.return_file_path("folder")
        for index, campaign in enumerate(self.folder_list):
            state = "disabled" if active_campaign.endswith(campaign) else "normal"
            fg_color = "light blue" if state == "disabled" else FGCOLOR

            switch_cmd = partial(self._switch_and_refresh, campaign)
            remove_cmd = partial(self._delete_and_refresh, campaign, active_campaign)

            switch_button = PackagedWidget(
                widget_type=ctk.CTkButton,
                text=campaign,
                state=state,
                command=switch_cmd,
                fg_color=fg_color,
                text_color_disabled="grey",
                text_color="black"
            )
            remove_button = PackagedWidget(
                widget_type=ctk.CTkButton,
                text="-",
                command=remove_cmd,
                width=15
            )
            row = Row(master=self, object_list=[switch_button, remove_button], weights=[1, 1])
            row.grid(row=index, column=0)
            self.row_list.append(row)

    def _switch_and_refresh(self, campaign):
        self.cmp.switch_campaign(campaign)
        self._refresh()

    def _delete_and_refresh(self, campaign, active_campaign):
        if active_campaign.endswith(campaign):
            others = [c for c in self.folder_list if c != campaign]
            if others:
                self.cmp.switch_campaign(others[0])
            else:
                error_subwindow(
                    master=self,
                    message="Cannot delete last campaign."
                )
                return

        self.cmp.delete_campaign(campaign)
        self._refresh()

    def _refresh(self):
        for row in self.row_list:
            row.destroy()

        self.row_list = []

        self._build_list()
        self.master.master.master.master.master.master.master.refresh_content()


class CampaignHandler:
    def __init__(self):
        self.dirs = DirPaths()

    def verify_paths_folder(self) -> bool:
        return os.path.exists(self.dirs.data)

    def build_campaign_list(self) -> list[str]:
        campaign_folder_list: list[str] = os.listdir(self.dirs.data)

        if "smiles_strings.yaml" in campaign_folder_list:
            campaign_folder_list.remove("smiles_strings.yaml")

        return campaign_folder_list

    def switch_campaign(self, new_campaign_name):
        self.dirs.build_campaign_folder(new_campaign_name)

    def delete_campaign(self, campaign_name):
        path = os.path.join(self.dirs.data, campaign_name)
        if os.path.exists(path):
            shutil.rmtree(path)

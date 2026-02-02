import yaml

import customtkinter as ctk

from src.environment.dir_paths import DirPaths
from src.gui.help.help_topic import HelpTopic
from src.gui.main.gui_constants import SUBHEADER


class HelpFrame(ctk.CTkFrame):
    def __init__(self, master=None):
        super().__init__(master)

        self.scrollframe = ctk.CTkScrollableFrame(master=self, width=600, height=400)
        self.scrollframe.columnconfigure(0, weight=1)
        self.scrollframe.pack()

        topic_dict = self._build_topic_dict()

        self._display_all_topics(topic_dict)

    def _display_all_topics(self, topic_dict=None):

        if topic_dict is None:
            topic_dict = {"Placeholder": "Placeholder text"}

        all_topics = [t for t in topic_dict.keys()]
        all_topics.sort()

        for index, topic in enumerate(all_topics):
            delimiter = "\n"
            text = delimiter.join(topic_dict[topic])
            t = HelpTopic(
                master=self.scrollframe,
                title=topic,
                content=text
            )

            pady = (10, 0) if index < len(all_topics) - 1 else 10
            t.grid(row=index, column=0, pady=pady, padx=10, sticky="ew")

    @staticmethod
    def _build_topic_dict() -> dict[str, str]:
        dirs = DirPaths()
        path = dirs.help

        with open(path) as f:
            topic_dict = yaml.safe_load(f)

        return topic_dict


def error_subwindow(master, message: str):
    subwindow = ctk.CTkToplevel(master)
    subwindow.title("Error")
    subwindow.grab_set()
    subwindow.focus_set()
    subwindow.label = ctk.CTkLabel(
        master=subwindow,
        text=message,
        font=SUBHEADER
    )
    subwindow.label.pack(
        pady=50, padx=50
    )

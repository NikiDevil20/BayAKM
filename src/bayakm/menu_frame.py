import customtkinter as ctk
from help_frame import HelpFrame
from new_campaign_frame import NewCampaignFrame
from param_view_frame import ParamViewFrame

class MainFrame(ctk.CTkFrame):
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
        self._create_subwindows()

    def _create_subwindows(self):
        btn_config = [
            ("New campaign", lambda: self._create_subwindow(name="New campaign")),
            ("New recommendation", lambda: test_func()),
            ("View Parameters", lambda: self._create_subwindow(name="View parameters")),
            ("Help", lambda: self._create_subwindow(name="Help"))
        ]
        for i, (text, command) in enumerate(btn_config):
            button = ctk.CTkButton(
                master=self,
                text=text,
                command=command,
                font=("Arial", 18),
                text_color="black",
                height=40,
                width=200,
                fg_color="light blue"
            )
            button.grid(row=i, column=0, pady=5, padx=10)

    def _create_subwindow(self, name: str):
        match name:
            case "Help":
                frame_class = HelpFrame
            case "New campaign":
                frame_class = NewCampaignFrame
            case "View parameters":
                frame_class = ParamViewFrame
            case _:
                raise ValueError()
        subwindow = ctk.CTkToplevel(self)
        subwindow.title(name)
        subwindow.grab_set()
        subwindow.focus_set()
        subwindow.columnconfigure(0, weight=1)
        subwindow.rowconfigure(0, weight=1)
        subwindow.frame = frame_class(subwindow)
        subwindow.frame.grid(row=0, column=0, sticky="nsew")

def test_func():
    print("Test.")



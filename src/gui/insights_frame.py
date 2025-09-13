import tkinter as tk
from typing import Literal

import customtkinter as ctk
from baybe.insights import SHAPInsight
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from src.bayakm.bayakm_campaign import load_campaign
from src.gui.gui_constants import TEXTCOLOR, FGCOLOR, STANDARD
from src.gui.new_page_factory import BaseFrame

HEADER = "Get insights"
PLOTTYPE: Literal["bar", "beeswarm", "force", "heatmap", "scatter", "waterfall"] = "bar"
GENERATE_BTN_TEXT = "Generate insight plot"
REGENERATE_BTN_TEXT = "Regenerate plot with new settings"
settings_dict = {"plot_type": "bar", "show": False, "data": None, "explanation_index": 0}
RADIO_TEXT_DISPLAY = "Display plot in app"
RADIO_TEXT_SAVE = "Save plot to file"
TESTTEXT = "Test"


class InsightsFrame(BaseFrame):
    def __init__(self, master):
        super().__init__(master)

        self.plotstate: bool = False
        self.settings_dict = settings_dict
        self.radio_var = tk.IntVar(value=0)
        self.button_frame = None
        self.plot_frame = None
        self.type_menu = None
        self.canvas = None
        self.campaign = load_campaign()
        self.insights = SHAPInsight.from_campaign(self.campaign)

        self.fill_content()

    def fill_content(self):
        self.header = HEADER
        self.build_frames()

        self.create_settings_frame()
        self.create_generate_button()

    def create_plot(self, kwargs):
        axes = self.insights.plot(
            self.settings_dict["plot_type"],  # Type: ignore
            **kwargs
        )
        fig = axes.figure

        fig.tight_layout()
        self.canvas = FigureCanvasTkAgg(fig, master=self.plot_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row=0, column=0)

        self.plotstate = True

        self.button_frame.destroy()
        self.create_generate_button()
        plt.close(fig)

    def plot_factory(self):
        if self.plotstate:
            self.plot_frame.destroy()

        self.plot_frame = ctk.CTkFrame(master=self.content_frame)
        self.plot_frame.grid(row=0, column=0, pady=5, padx=10)

        self.settings_dict["plot_type"] = self.type_menu.get()

        kwargs = {"show": self.settings_dict["show"]}

        match self.settings_dict["plot_type"]:
            case "force" | "waterfall":
                kwargs["explanation_index"] = self.settings_dict["explanation_index"]
                self.create_plot(kwargs)
            case _:
                self.create_plot(kwargs)

    def create_generate_button(self):
        self.button_frame = ctk.CTkFrame(master=self.bottom_frame)
        self.button_frame.grid(row=0, column=0, pady=5, padx=10)

        if not self.plotstate:
            self.create_generic_button(
                master=self.button_frame,
                text=GENERATE_BTN_TEXT,
                command=self.plot_factory,
                row=1
            )
        else:
            self.create_generic_button(
                master=self.button_frame,
                text=REGENERATE_BTN_TEXT,
                command=self.plot_factory,
                row=1
            )
        self.create_generic_button(
            master=self.button_frame,
            text=TESTTEXT,
            command=lambda: print(self.radio_var.get()),
            row=2
        )

    def create_settings_frame(self):
        frame = ctk.CTkFrame(master=self.content_frame)
        frame.grid(row=0, column=1, pady=5, padx=10)

        self.type_menu = ctk.CTkOptionMenu(
            master=frame,
            values=["bar", "beeswarm", "force", "heatmap", "scatter", "waterfall"],
            text_color=TEXTCOLOR,
            fg_color=FGCOLOR,
        )
        self.type_menu.grid(row=0, column=0, pady=5, padx=10)

        self.create_radio_buttons(master=frame)

    def create_radio_buttons(self, master):
        radiobutton_1 = ctk.CTkRadioButton(
            master=master,
            text=RADIO_TEXT_DISPLAY,
            value=0,
            variable=self.radio_var,

        )
        radiobutton_1.select()
        radiobutton_2 = ctk.CTkRadioButton(
            master=master,
            text=RADIO_TEXT_SAVE,
            value=1,
            variable=self.radio_var
        )
        radiobutton_1.grid(row=1, column=0, pady=5, padx=10, sticky="w")
        radiobutton_2.grid(row=2, column=0, pady=5, padx=10, sticky="w")


    # TODO implement functionality of buttons

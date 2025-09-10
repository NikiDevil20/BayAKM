import tkinter as tk
from typing import Literal

import customtkinter as ctk
from baybe.insights import SHAPInsight
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from src.bayakm.bayakm_campaign import load_campaign
from src.gui.gui_constants import TEXTCOLOR, FGCOLOR, STANDARD
from src.gui.new_page_factory import BaseFrame

HEADER = "Get insights"
PLOTTYPE: Literal["bar", "beeswarm", "force", "heatmap", "scatter", "waterfall"] = "bar"
BUTTON_TEXT = "Generate insight plot"
settings_dict = {"plottype": "bar", "show": False, "data": None, "expl_index": None}
RADIO_TEXT_DISPLAY = "Display plot in app"
RADIO_TEXT_SAVE = "Save plot to file"


class InsightsFrame(BaseFrame):
    def __init__(self, master):
        super().__init__(master)

        self.plotstate: bool = False
        self.settings_dict = settings_dict

        self.fill_content()

    def fill_content(self):
        self.header = HEADER
        self.build_frames()

        self.create_settings_frame()
        self.create_generate_button()

    def create_plot(self):
        if self.plotstate:
            return

        campaign = load_campaign()
        insight = SHAPInsight.from_campaign(campaign)

        axes = insight.plot(PLOTTYPE, show=False)  # Gibt ein Axes-Objekt zurück
        fig = axes.figure

        fig.tight_layout()
        canvas = FigureCanvasTkAgg(fig, master=self.content_frame)
        canvas.draw()
        canvas.get_tk_widget().grid(row=0, column=0)

        self.plotstate = True

    def create_generate_button(self):
        button_frame = ctk.CTkFrame(master=self.bottom_frame)
        button_frame.grid(row=0, column=0, pady=5, padx=10)

        self.create_generic_button(
            master=button_frame,
            text=BUTTON_TEXT,
            command=self.create_plot
        )

    def create_settings_frame(self):
        frame = ctk.CTkFrame(master=self.content_frame)
        frame.grid(row=0, column=1, pady=5, padx=10)

        type_menu = ctk.CTkOptionMenu(
            master=frame,
            values=["bar", "beeswarm", "force", "heatmap", "scatter", "waterfall"],
            text_color=TEXTCOLOR,
            fg_color=FGCOLOR,
        )
        type_menu.grid(row=0, column=0, pady=5, padx=10)

        self.create_radio_buttons(master=frame)

    @staticmethod
    def create_radio_buttons(master):
        radio_var = tk.IntVar(value=0)
        radiobutton_1 = ctk.CTkRadioButton(
            master=master,
            text=RADIO_TEXT_DISPLAY,
            value=1,
            variable=radio_var
        )
        radiobutton_2 = ctk.CTkRadioButton(
            master=master,
            text=RADIO_TEXT_SAVE,
            value=2,
            variable=radio_var
        )
        radiobutton_1.grid(row=1, column=0, pady=5, padx=10, sticky="w")
        radiobutton_2.grid(row=2, column=0, pady=5, padx=10, sticky="w")

    # TODO implement functionality of buttons

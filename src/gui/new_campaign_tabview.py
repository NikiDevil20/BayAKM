import customtkinter as ctk

from src.bayakm.config_loader import Config
from src.gui.param_view_frame import create_full_table
from src.bayakm.parameters import build_param_list
from src.gui.add_numerical_frame import AddNumericalFrame
from src.gui.remove_parameter_frame import RemoveParameterFrame
from src.gui.add_substance_frame import AddSubstanceFrame
from src.bayakm.bayakm_campaign import BayAKMCampaign


class NewCampaignTabview(ctk.CTkTabview):
    def __init__(self, master=None, parameter_list=None):
        super().__init__(master)

        self.parameter_list = parameter_list
        self.cfg = Config()

        self._segmented_button.configure(font=ctk.CTkFont(family="Arial", size=12, weight="bold"))
        self.configure(
            text_color="black",
            anchor="nw"
        )
        self.add("Configuration")
        self.add("Parameters")
        self.add("Get recommendation")

        self._create_widget_frame()
        self._create_widgets()
        self._setup_parameters_frame()
        self._create_recommendation_frame()

    def _create_widget_frame(self):
        self.widget_frame = ctk.CTkFrame(
            master=self.tab("Configuration"),
            fg_color="dark grey"
        )
        self.widget_frame.grid(row=0, column=0, pady=10, padx=30)

    def _create_widgets(self):
        self.widget_list = []
        widget_config = (
            ("Choose acquisition function", ctk.CTkOptionMenu, None, {"values": ("qLogEI", "UCB", "qPI")}),
            ("Batchsize", ctk.CTkEntry, 1, {}),
            ("Show probability of improvement", ctk.CTkCheckBox, True, {})
        )
        for i, (widget_name, widget_type, widget_default, widget_kwargs) in enumerate(widget_config):
            label = ctk.CTkLabel(
                master=self.widget_frame,
                text=widget_name,
                text_color="black",
                width=150
            )
            widget = widget_type(
                master=self.widget_frame,
                **widget_kwargs,
                text_color="black",
                width=150
            )
            self.widget_list.append(widget)
            if isinstance(widget, ctk.CTkEntry):
                widget.insert(0, widget_default)
            if isinstance(widget, ctk.CTkCheckBox):
                widget.configure(
                    text=""
                )
                if widget_default:
                    widget.select()
                else:
                    widget.deselect()
            if isinstance(widget, ctk.CTkOptionMenu):
                widget.set(widget_default)
            label.grid(row=i+1, column=0, pady=2, padx=10)
            widget.grid(row=i+1, column=1, pady=2, padx=10)

    def _setup_parameters_frame(self):
        self.setup_frame = ctk.CTkFrame(master=self.tab("Parameters"))
        self.setup_frame.pack(pady=5, padx=10)

        self._build_parameters()

        if not self.parameter_list:
            no_parameters_label = ctk.CTkLabel(
                master=self.parameter_frame,
                text="Use the buttons below to add some parameters."
            )
            no_parameters_label.pack()

        button_frame = ctk.CTkFrame(master=self.tab("Parameters"))
        button_frame.pack(side="left", pady=5, padx=10)

        btn_config = (
            ("Add Numerical", {"master": self, "title": "Add numerical parameter", "frameclass": AddNumericalFrame}),
            ("Add Substance", {"master": self, "title": "Add numerical parameter", "frameclass": AddSubstanceFrame}),
            ("Remove", {"master": self, "title": "Add numerical parameter", "frameclass": RemoveParameterFrame}),
        )
        for i, (text, kwargs) in enumerate(btn_config):
            button = ctk.CTkButton(
                master=button_frame, text=text, width=50, text_color="black",
                command=lambda arguments=kwargs: create_subwindow(**arguments))
            button.grid(row=0, column=i, pady=2, padx=5)

    def _build_parameters(self):
        self.parameter_frame = ctk.CTkScrollableFrame(
            master=self.setup_frame,
            width=400,
            orientation="horizontal"
        )
        self.parameter_frame.grid(row=0, column=0)

        create_full_table(self.parameter_frame, self.parameter_list)

    def refresh_parameters(self):
        self.parameter_list = build_param_list()
        self.parameter_frame.destroy()
        self._build_parameters()

    def _create_recommendation_frame(self):
        recommendation_frame = ctk.CTkFrame(master=self.tab("Get recommendation"))
        recommendation_frame.pack(pady=5, padx=10)
        recommendation_button = ctk.CTkButton(
            master=recommendation_frame,
            text="Get first recommendation",
            width=100,
            height=70,
            command=lambda: self._save_and_get_recommendation()
        )
        recommendation_button.pack()

    def _save_and_get_recommendation(self):
        campaign = BayAKMCampaign()
        campaign.get_recommendation(initial=True)
        self.master.master.master.refresh_content()


def create_subwindow(master, title, frameclass):
    subwindow = ctk.CTkToplevel(master)
    subwindow.title(title)
    subwindow.grab_set()
    subwindow.focus_set()
    subwindow.columnconfigure(0, weight=1)
    subwindow.rowconfigure(0, weight=1)
    subwindow.frame = frameclass(master=subwindow)
    subwindow.frame.grid(row=0, column=0, sticky="nsew")
    return subwindow

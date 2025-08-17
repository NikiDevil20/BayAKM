import customtkinter as ctk

from src.bayakm.param_view_frame import create_full_table
from src.bayakm.parameters import build_param_list
from src.bayakm.add_numerical_frame import AddNumericalFrame
from src.bayakm.remove_parameter_frame import RemoveParameterFrame


class NewCampaignTabview(ctk.CTkTabview):
    def __init__(self, master=None, parameter_list=None):
        super().__init__(master)

        self.parameter_list = parameter_list

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

    def _create_widget_frame(self):
        self.widget_frame = ctk.CTkFrame(
            master=self.tab("Configuration"),
            fg_color="dark grey"
        )

        for row in range(6):
            self.widget_frame.rowconfigure(row, weight=1)
        for col in range(6):
            self.widget_frame.columnconfigure(col, weight=1)
        self.widget_frame.grid(row=0, column=0, pady=10, padx=30)

    def _create_widgets(self):
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

        for row in range(2):
            self.setup_frame.rowconfigure(row, weight=1)
        for col, _ in enumerate(self.parameter_list):
            self.setup_frame.columnconfigure(col, weight=1)

        self._build_parameters()

        button_frame = ctk.CTkFrame(master=self.tab("Parameters"))
        button_frame.pack(side="left", pady=5, padx=10)

        btn_config = (
            ("Add Numerical", {"master": self, "title": "Add numerical parameter", "frameclass": AddNumericalFrame}),
            ("Add Substance", {"master": self, "title": "Add numerical parameter", "frameclass": AddNumericalFrame}),
            ("Remove", {"master": self, "title": "Add numerical parameter", "frameclass": RemoveParameterFrame}),
        )
        for i, (text, kwargs) in enumerate(btn_config):
            button = ctk.CTkButton(
                master=button_frame, text=text, width=50, text_color="black",
                command=lambda arguments=kwargs: create_subwindow(**arguments))
            button.grid(row=0, column=i, pady=2, padx=5)

    def _build_parameters(self):
        self.parameter_frame = ctk.CTkFrame(master=self.setup_frame)
        self.parameter_frame.grid(row=0, column=0)

        create_full_table(self.parameter_frame, self.parameter_list)

    def _refresh_parameters(self):
        self.parameter_list = build_param_list()
        self.parameter_frame.destroy()
        self._build_parameters()

    def _save_and_get_recommendation(self):
        pass


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

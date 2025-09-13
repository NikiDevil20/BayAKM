import customtkinter as ctk

from src.bayakm.config_loader import Config
from src.bayakm.dir_paths import DirPaths
from src.bayakm.output import check_path
from src.bayakm.parameters import build_param_list
from src.gui.gui_constants import STANDARD, SUBHEADER
from src.gui.parameter_frames.new_continuous_frame import NewContinuousParameterFrame
from src.gui.parameter_frames.new_numerical_frame import NewNumericalParameterFrame
from src.gui.parameter_frames.new_substance_frame import NewSubstanceParameterFrame
from src.gui.parameter_frames.param_view_frame import create_full_table
from src.gui.parameter_frames.remove_parameter_frame import RemoveParameterFrame


class NewCampaignTabview(ctk.CTkTabview):
    def __init__(self, master=None, parameter_list=None):
        super().__init__(master)

        self.parameter_list = parameter_list
        self.cfg = Config()
        self.dirs = DirPaths()
        self.widgets_dict = {}

        self._segmented_button.configure(
            font=ctk.CTkFont(
                family="Inter",
                size=16,
                # weight="bold"
            ),
            fg_color="light grey",
            corner_radius=10
        )
        self.configure(
            text_color="black",
            anchor="nw",
            height=20,
            segmented_button_selected_color="light blue",
            segmented_button_unselected_color="light grey"
        )
        self.add("Configuration")
        self.add("Parameters")
        self.add("Get recommendation")

        self._create_widget_frame()
        self._setup_parameters_frame()
        self._create_recommendation_frame()

    def _create_widget_frame(self):
        self.widget_frame = ctk.CTkFrame(
            master=self.tab("Configuration"),
            fg_color="light grey"
        )
        self.widget_frame.grid(
            row=0, column=0,
            pady=10, padx=30
        )
        self._create_widgets()

        save_button = ctk.CTkButton(
            master=self.widget_frame,
            command=lambda: self._save_config(),
            text="Save config",
            text_color="black",
        )
        save_button.grid(
            row=len(self.widgets_dict.keys())+1, column=0,
            pady=5, padx=10,
            columnspan=2, sticky="ew"
        )

    def _create_widgets(self):
        self.widget_list = []
        widget_config = (
            ("Journal prefix", ctk.CTkEntry, self.cfg.dict["Journal prefix"], {}),
            ("Batchsize", ctk.CTkEntry, self.cfg.dict["Batchsize"], {}),
            ("Initial recommender", ctk.CTkOptionMenu, self.cfg.dict["Initial recommender"],
             {"values": ("FPS", "Random")}),
            ("Acquisition function", ctk.CTkOptionMenu, self.cfg.dict["Acquisition function"],
             {"values": ("qLogEI", "UCB", "qPI")}),
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
                width=150,
            )

            if isinstance(widget, ctk.CTkEntry):
                widget.configure(fg_color="white")
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
                widget.configure(fg_color="light blue")
                widget.set(widget_default)

            self.widgets_dict[widget_name] = widget

            label.grid(
                row=i+1, column=0,
                pady=2, padx=10
            )
            widget.grid(
                row=i+1, column=1,
                pady=2, padx=10
            )

    def _save_config(self):
        _new_dict = {}
        for key in self.widgets_dict.keys():
            _new_dict[key] = self.widgets_dict[key].get()
        self.cfg.save_to_yaml(_new_dict)

    def _setup_parameters_frame(self):
        self.setup_frame = ctk.CTkFrame(master=self.tab("Parameters"))
        self.setup_frame.pack(pady=5, padx=10)

        self._build_parameters()

        if not self.parameter_list:
            no_parameters_label = ctk.CTkLabel(
                master=self.parameter_frame,
                text="Use the buttons below to add some parameters."
            )
            no_parameters_label.grid(
                row=0, column=0,
                pady=5, padx=10
            )

        button_frame = ctk.CTkFrame(master=self.setup_frame)
        button_frame.grid(
            row=1, column=0,
            pady=5, padx=10,
            sticky="ew"
        )

        btn_config = (
            ("Add Numerical", {"master": self, "title": "Add numerical parameter", "frameclass": "numerical"}),
            ("Add Substance", {"master": self, "title": "Add substance parameter", "frameclass": "substance"}),
            ("Add Continuous", {"master": self, "title": "Add continous parameter", "frameclass": "continuous"}),
            ("Remove", {"master": self, "title": "Remove parameter", "frameclass": "remove"})
        )
        for i, (text, kwargs) in enumerate(btn_config):
            if i == 2 and not check_path(self.dirs.param_path):
                return
            button = ctk.CTkButton(
                master=button_frame,
                text=text,
                width=50,
                text_color="black",
                command=lambda arguments=kwargs: create_subwindow(**arguments),
                fg_color="light blue",
                font=STANDARD
            )
            button.grid(
                row=0, column=i,
                pady=5, padx=10
            )

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
        self.setup_frame.destroy()
        self._setup_parameters_frame()

    def _create_recommendation_frame(self):
        recommendation_frame = ctk.CTkFrame(master=self.tab("Get recommendation"))
        recommendation_frame.pack(pady=5, padx=10)
        recommendation_button = ctk.CTkButton(
            master=recommendation_frame,
            text="Get first recommendation",
            width=100,
            height=70,
            command=lambda: self._save_and_get_recommendation(),
            font=SUBHEADER,
            fg_color="light blue",
            text_color="black"
        )
        recommendation_button.pack()

    def _save_and_get_recommendation(self):
        self._save_config()
        self.master.master.master.command_save_campaign_and_get_first_recommendation()


def create_subwindow(
        master,
        title,
        frameclass
):
    subwindow = ctk.CTkToplevel(master)
    subwindow.title(title)
    subwindow.grab_set()
    subwindow.focus_set()

    subwindow.frame = frame_factory(subwindow, frameclass)

    subwindow.frame.grid(row=0, column=0, sticky="nsew")
    return subwindow


def frame_factory(master, child):
    if child == "substance":
        frame = NewSubstanceParameterFrame(master)
    elif child == "numerical":
        frame = NewNumericalParameterFrame(master)
    elif child == "remove":
        frame = RemoveParameterFrame(master)
    elif child == "continuous":
        frame = NewContinuousParameterFrame(master)
    else:
        raise ValueError("Unknown frame type")

    frame.fill_content()
    return frame

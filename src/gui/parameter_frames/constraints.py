import customtkinter as ctk
from baybe.constraints import DiscreteExcludeConstraint, ThresholdCondition, SubSelectionCondition
from baybe.parameters import SubstanceParameter, NumericalDiscreteParameter, NumericalContinuousParameter

from src.bayakm.parameters import write_to_parameters_file, write_constraints_to_file
from src.gui.main_gui.gui_constants import STANDARD, FGCOLOR, TEXTCOLOR
from src.gui.help import error_subwindow
from src.gui.main_gui.new_page_factory import BaseFrame
from src.gui.main_gui.gui_constants import Row, PackagedWidget

HEADER_PLACEHOLDER = "Add constraint"


class ConstraintsFrame(BaseFrame):
    def __init__(self, master):
        super().__init__(master)
        self.parameter_list = self.master.master.parameter_list

    def fill_content(self):
        self.header = HEADER_PLACEHOLDER
        self.build_frames()

        param_window = ParameterWindow(
            master=self.content_frame,
            parameter_list=self.parameter_list
        )
        param_window.grid(row=0, column=0, sticky="ew")
        param_window.build_widgets()

        combiner = ctk.CTkOptionMenu(
            master=self.content_frame,
            values=["AND", "OR"],
            font=STANDARD,
            fg_color=FGCOLOR,
            text_color=TEXTCOLOR,
            width=30
        )

        other_param_window = ParameterWindow(
            master=self.content_frame,
            parameter_list=self.parameter_list
        )
        other_param_window.grid(row=0, column=1, sticky="ew")
        other_param_window.build_widgets()

        save_button = ctk.CTkButton(
            master=self.bottom_frame,
            command=lambda: self._save_constraint(
                param_window,
                other_param_window,
                combiner.get()
            ),
            text="Save constraint",
            text_color=TEXTCOLOR,
            fg_color=FGCOLOR,
            font=STANDARD,
        )
        save_button.grid(row=0, column=0, pady=5, padx=5)

    def _save_constraint(self, param_window_1, param_window_2, combiner="AND"):
        write_constraints_to_file(
            first_condition=param_window_1.build_condition(),
            second_condition=param_window_2.build_condition(),
            combiner=combiner
        )
        self.master.destroy()


class ParameterWindow(ctk.CTkFrame):
    def __init__(self, master, parameter_list):
        super().__init__(master)
        self.param_choice = None
        self.lower_frame = None
        self.parameter_list = parameter_list
        self.param_name_list = self._build_param_name_list()
        self.param_value_list = None
        self.constraint_list = []

    def _build_param_name_list(self):
        return [p.name for p in self.parameter_list]

    def _build_param_value_list(self):
        self.mode = self._choose_mode()
        match self.mode:
            case "substance":
                self.param_value_list = self.current_param.data.keys()
            case "numerical":
                self.param_value_list = self.current_param.values
            case None:
                self.param_value_list = None
            case _:
                error_subwindow(master=self, message="Unknown parameter type selected.")

    def build_widgets(self):
        self.param_choice = ctk.CTkOptionMenu(
            master=self,
            values=self.param_name_list,
            command=self._refresh
        )
        self.param_choice.grid(row=0, column=0, pady=5, padx=5, sticky="w")
        self.param_choice.set("Select parameter")

    def _current_param_object(self):
        current_selection = self.param_choice.get()
        if current_selection == "Select parameter":
            return None

        for param in self.parameter_list:
            if param.name == current_selection:
                return param
        return None

    def _choose_mode(self):
        self.current_param = self._current_param_object()
        if isinstance(self.current_param, SubstanceParameter):
            return "substance"
        elif isinstance(self.current_param, NumericalDiscreteParameter):
            return "numerical"
        else:
            return None

    def _refresh(self, name):
        if self.lower_frame is not None:
            self.lower_frame.destroy()
        self._build_param_value_list()
        self.lower_frame = LowerFrame(master=self)
        self.lower_frame.grid(row=1, column=0, pady=5, padx=5)
        self.lower_frame.build_lower_frame(
            mode=self._choose_mode(),
            value_list=self.param_value_list
        )
        self.widget_list = self.lower_frame.widget_list

    def build_condition(self):
        match self.mode:
            case "substance":
                selected_values = list(
                    checkbox.cget("text")
                    for checkbox in self.widget_list
                    if checkbox.get()
                )
                condition = {
                    "type": "subselection",
                    "selection": selected_values,
                    "operator": None,
                    "threshold": None
                }
                return self.current_param.name, condition
            case "numerical":
                operator = self.widget_list[0].get()
                value = float(self.widget_list[1].get())
                condition = {
                    "type": "threshold",
                    "selection": None,
                    "operator": operator,
                    "threshold": value
                }
                return self.current_param.name, condition
            case _:
                error_subwindow(master=self, message="Unknown parameter type selected.")
                return None


class LowerFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.mode = None
        self.widget_list = None

    def build_lower_frame(self, mode, value_list):
        self.mode = mode
        match self.mode:
            case "substance":
                widget = ValueChoiceList(
                    master=self,
                    value_list=value_list,
                    height=150
                )
                widget.pack(pady=5, padx=5, fill="both", expand=True)
                self.widget_list = widget.return_checkbox_list()
            case "numerical":
                operator = ctk.CTkOptionMenu(
                    master=self,
                    values=["<", "<=", "=", ">=", ">"],
                    font=STANDARD,
                    fg_color=FGCOLOR,
                    text_color=TEXTCOLOR,
                    width=30
                )
                operator.grid(row=0, column=0, pady=5, padx=5, sticky="w")
                value_entry = ctk.CTkEntry(
                    master=self,
                    font=STANDARD,
                    fg_color=FGCOLOR,
                    text_color=TEXTCOLOR
                )
                value_entry.grid(row=0, column=1, pady=5, padx=5, sticky="w")
                self.widget_list = [operator, value_entry]
            case _:
                error_subwindow(master=self, message="Unknown parameter type selected.")


class ValueChoiceList(ctk.CTkScrollableFrame):
    def __init__(self, master, value_list, **kwargs):
        super().__init__(master, **kwargs)
        self.value_list = value_list

    def _build_list(self):
        self.check_box_list = []
        for index, value in enumerate(self.value_list):
            checkbox = PackagedWidget(
                ctk.CTkCheckBox,
                text=str(value),
                font=STANDARD,
                fg_color=FGCOLOR,
                text_color=TEXTCOLOR
            )
            row = Row(
                master=self,
                object_list=[checkbox],
                weights=[1]
            )
            row.grid(row=index, column=0, pady=2, padx=5, sticky="ew")
            self.check_box_list.append(row.return_widget(0))

    def return_checkbox_list(self):
        self._build_list()
        return self.check_box_list


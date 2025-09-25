import customtkinter as ctk
from baybe.constraints import DiscreteExcludeConstraint, ThresholdCondition, SubSelectionCondition
from baybe.parameters import SubstanceParameter, NumericalDiscreteParameter, NumericalContinuousParameter
from numba.core.compiler_machinery import pass_info

from src.bayakm.parameters import write_to_parameters_file
from src.gui.main_gui.gui_constants import STANDARD, FGCOLOR, TEXTCOLOR
from src.gui.help import error_subwindow
from src.gui.main_gui.new_page_factory import BaseFrame

HEADER_PLACEHOLDER = "Add constraint"
ERROR_MESSAGE = "Wrong parameter type"


class ConstraintsFrame(BaseFrame):
    def __init__(self, master):
        super().__init__(master)
        # self.parameter_list = self.master.master.parameter_list

    def fill_content(self):
        self.header = HEADER_PLACEHOLDER
        self.build_frames()
        row = ConstraintRow(master=self.content_frame)
        row.grid(row=0, column=0, pady=5, padx=10)


class ConstraintRow(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.frame = ctk.CTkFrame(
            master=self
        )
        self.frame.grid(row=0, column=0, pady=5, padx=10)

        self.parameter_list = self.master.master.master.master.parameter_list  # :)
        self.name_list = [parameter.name for parameter in self.parameter_list]

        self.current = self.parameter_list[0]

        self._display_param_name_menu(0)
        self._display_values(1)

        self._operator_menu(3)

    def _remove(self):
        pass

    def _save(self):
        pass

    def _construct_constraint(self):
        pass

    @staticmethod
    def _choose_discrete_condition_type(parameter) -> ThresholdCondition | SubSelectionCondition:
        if parameter["type"] == "numerical":
            condition = ThresholdCondition(
                threshold=parameter["threshold"],
                operator=parameter["operator"]
            )
        else:
            condition = SubSelectionCondition(
                selection=parameter["selection"]
            )
        return condition

    @staticmethod
    def _choose_cont_condition_type(parameter):
        NotImplementedError()  # TODO

    def disc_excl_constraint(self, parameter: dict, other_parameter: dict) -> DiscreteExcludeConstraint:
        constraint = DiscreteExcludeConstraint(
            parameters=[parameter["name"], other_parameter["name"]],
            combiner="AND",
            conditions=[
                self._choose_discrete_condition_type(parameter),
                self._choose_discrete_condition_type(other_parameter)
            ]
        )
        return constraint

    def _display_param_name_menu(self, col):
        values = ([parameter.name for parameter in self.parameter_list
                   if not isinstance(parameter, NumericalContinuousParameter)])
        self.parameter = self._display_optionmenu(
            values=values,
            master=self.frame,
            column=col,
            command=self.set_current_param
        )

    def set_current_param(self, choice):
        self.current = [param for param in self.parameter_list if param.name == choice][0]
        # if self.frame is not None:
        #     self.frame.destroy()
        self._display_values(1)

    def _display_values(self, col):
        if self.current is None:
            return

        if isinstance(self.current, SubstanceParameter):
            filtered_param = [param for param in self.parameter_list if param.name == self.current.name]
            value_list = [name for name in filtered_param[0].data.keys()]

        elif isinstance(self.current, NumericalDiscreteParameter):
            value_list = [str(value) for value in self.current.values]

        else:
            value_list = None
            error_subwindow(master=self, message=ERROR_MESSAGE)

        self.value = self._display_optionmenu(
            master=self.frame,
            values=value_list,
            column=col,
            command=None
        )

    @staticmethod
    def _display_optionmenu(master, values, column, command):
        param_name_menu = ctk.CTkOptionMenu(
            master=master,
            values=values,
            fg_color=FGCOLOR,
            font=STANDARD,
            command=command,
            text_color=TEXTCOLOR
        )
        param_name_menu.grid(row=0, column=column, pady=5, padx=10)
        return param_name_menu

    def _operator_menu(self, col):
        self.operator = self._display_optionmenu(
            master=self.frame,
            values=["<", "=", ">"],
            column=col,
            command=None
        )



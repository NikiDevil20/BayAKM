import customtkinter as ctk
from src.bayakm.parameters import build_param_list
from baybe.parameters import SubstanceParameter, NumericalDiscreteParameter


class ParamViewFrame(ctk.CTkFrame):
    def __init__(self, params, master=None):
        super().__init__(master)

        parameter_list = params
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)

        for i, _ in enumerate(parameter_list):
            self.columnconfigure(i, weight=1)

        self._create_full_table(parameter_list)

        label = ctk.CTkLabel(master=self, text="View parameters", font=("Arial", 24))
        label.grid(column=0, row=0, columnspan=len(parameter_list), padx=10, pady=10)

        info_text = ctk.CTkLabel(
            master=self,
            text="Parameters can only be changed by starting a new campaign.",
            font=("Arial", 14)
        )
        info_text.grid(column=0, row=2, columnspan=len(parameter_list), padx=10, pady=5)

    def _create_full_table(
            self,
            parameter_list: list[NumericalDiscreteParameter | SubstanceParameter]
    ):
        for i, param in enumerate(parameter_list):
                self._create_block(i, param)

    def _create_block(
            self,
            column: int,
            parameter: NumericalDiscreteParameter | SubstanceParameter
    ):
        block = ctk.CTkFrame(master=self)
        block.columnconfigure(0, weight=1)

        for row in range(len(parameter.values)+1):
            block.rowconfigure(row, weight=1)
        label = ctk.CTkLabel(master=block, text=parameter.name, font=("Arial", 20))
        label.grid(row=0, column=0, pady=4, padx=10)
        for row in range(len(parameter.values)):
            value = ctk.CTkLabel(
                master=block,
                text=self._display_parameter_name(parameter.values[row])
            )
            value.grid(row=row+1, column=0, pady=1, padx=10)

        block.grid(row=1, column=column, pady=5, padx=10, sticky="n")

    @staticmethod
    def _display_parameter_name(value: str | float) -> str:
        if isinstance(value, float):
            return str(value)
        if not len(value) > 16:
            return value
        else:
            return value[0:12] + "..."

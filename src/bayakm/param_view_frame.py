import customtkinter as ctk
from src.bayakm.parameters import build_param_list
from baybe.parameters import SubstanceParameter, NumericalDiscreteParameter

class ParamViewFrame(ctk.CTkFrame):
    def __init__(self, master=None):
        super().__init__(master)

        label = ctk.CTkLabel(master=self, text="View parameters")
        label.pack()
        parameter_list = build_param_list()
        for param in parameter_list:
            self._create_block(param)

    def _create_block(
            self,
            parameter: NumericalDiscreteParameter | SubstanceParameter
    ):
        block = ctk.CTkFrame(master=self)
        if isinstance(parameter, NumericalDiscreteParameter):
            block.columnconfigure(0, weight=1)
        elif isinstance(parameter, SubstanceParameter):
            block.columnconfigure(0, weight=1)
            block.columnconfigure(1, weight=1)

        for row in range(len(parameter.values)+1):
            block.rowconfigure(row, weight=1)
        label = ctk.CTkLabel(master=block, text=parameter.name)
        label.pack(pady=5, padx=10)
        block.pack(pady=10, padx=10)
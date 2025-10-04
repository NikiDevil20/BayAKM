import customtkinter as ctk
from baybe.parameters import SubstanceParameter, NumericalDiscreteParameter, NumericalContinuousParameter

from src.gui.main_gui.gui_constants import SUBHEADER, HEADER, STANDARD


class ParamViewFrame(ctk.CTkFrame):
    def __init__(self, parameter_list, master=None):
        super().__init__(master)

        if parameter_list is None:
            no_parameter_label = ctk.CTkLabel(
                master=self,
                text="Start a campaign to display parameters.",
                font=HEADER
            )
            no_parameter_label.grid(
                column=0, row=0,
                pady=50, padx=50
            )
        else:
            for i, _ in enumerate(parameter_list):
                self.columnconfigure(i, weight=1)

            create_full_table(self, parameter_list)

            label = ctk.CTkLabel(
                master=self,
                text="View parameters",
                font=HEADER
            )
            label.grid(
                column=0, row=0,
                padx=10, pady=10,
                columnspan=len(parameter_list)
            )

            info_text = ctk.CTkLabel(
                master=self,
                text="Parameters can only be changed by starting a new campaign.",
                font=STANDARD
            )
            info_text.grid(
                column=0, row=2,
                padx=10, pady=5,
                columnspan=len(parameter_list)
            )


def create_full_table(
        master,
        parameter_list: list[NumericalDiscreteParameter | SubstanceParameter | NumericalContinuousParameter]
):
    if parameter_list is None:
        return
    for i, param in enumerate(parameter_list):
        create_block(master, i, param)


def create_block(
        master,
        column: int,
        parameter: NumericalDiscreteParameter | SubstanceParameter | NumericalContinuousParameter
):
    block = ctk.CTkFrame(master=master)
    block.columnconfigure(0, weight=1)

    # for row in range(len(parameter.values)+1):
    #     block.rowconfigure(row, weight=1)

    label = ctk.CTkLabel(
        master=block,
        text=parameter.name,
        font=SUBHEADER
    )
    label.grid(row=0, column=0, pady=5, padx=10)

    if not isinstance(parameter, NumericalContinuousParameter):
        for row in range(len(parameter.values)):
            value = ctk.CTkLabel(
                master=block,
                text=display_parameter_name(parameter.values[row])
            )
            value.grid(row=row+1, column=0, pady=1, padx=10)
    else:
        value = ctk.CTkLabel(
            master=block,
            text=f"{parameter.bounds.lower} - {parameter.bounds.upper}"
        )
        value.grid(row=1, column=0, pady=1, padx=10)

    block.grid(row=1, column=column, pady=5, padx=10, sticky="n")


def display_parameter_name(value: str | float) -> str:
    if isinstance(value, float):
        return str(value)
    if not len(value) > 16:
        return value
    else:
        return value[0:12] + "..."

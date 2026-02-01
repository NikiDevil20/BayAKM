import os
from pathlib import Path
from typing import Callable

import matplotlib.pyplot as plt

from src.environment.dir_paths import DirPaths
from src.logic.output.output import find_current_iteration


def save_plot(
        figure: plt.Figure,
        file_name: str
) -> None:
    """
    Saves a matplotlib figure to the specified filename within the plots directory.
    :param figure: The matplotlib figure to save.
    :param file_name: The name of the file to save the figure as.
    """
    dirs = DirPaths()
    path = dirs.return_file_path("folder")
    full = os.path.join(path, file_name)

    figure.savefig(full)
    plt.close(figure)


def command_save_plot(
        figure: plt.Figure,
        mode: str,
        insight_type: str = None
) -> Callable:
    """
    Saves a plot based on the current iteration and mode.
    :param figure: The matplotlib figure to save.
    :param mode: Specifies, what plot is sabed in what place.
    :param insight_type: Optional; The type of insight plot, if mode is "insight".
    """

    current_iteration = find_current_iteration()

    match mode:

        case "pi":
            file_name = f"pi_values_iteration_{current_iteration}.png"

        case "yield":
            file_name = f"yield_per_batch_iteration_{current_iteration}.png"

        case "insight":
            file_name = insight_type + f"_iteration_{current_iteration}.png"

        case _:
            raise ValueError(f"Mode {mode} not recognized.")

    return save_plot(figure=figure, file_name=file_name)

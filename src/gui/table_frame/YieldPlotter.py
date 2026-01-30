import matplotlib.pyplot as plt
import numpy as np


TITLE = "Yield per batch"
YLABEL = "Yield / %"
XLABEL = "Batch number"
LINECOLOR = "navy"
BGCOLOR = "skyblue"


class YieldPlotter:
    def __init__(self, data: list[list[float]]):
        self.data = np.array(data)

    def _unpack_data(self):
        self.means = self.data.mean(axis=1)
        self.mins = self.data.min(axis=1)
        self.maxs = self.data.max(axis=1)
        self.batches = np.arange(1, len(self.data) + 1)

    def create_plot(
            self,
            figsize: tuple[float, float] = (3, 2),
            base_fontsize: int = 10
    ):
        self._unpack_data()

        fig, ax = plt.subplots(figsize=figsize, layout="constrained")
        ax.plot(self.batches, self.means, label="Mean yield per batch")
        ax.fill_between(
            self.batches, self.mins, self.maxs,
            color=BGCOLOR, alpha=0.35, label="Range of yields"
        )

        ax.set_title(TITLE, fontsize=base_fontsize)
        ax.set_ylabel(YLABEL, fontsize=base_fontsize - 2)
        ax.set_xlabel(XLABEL, fontsize=base_fontsize - 2)

        ax.set_xticks(self.batches)
        ax.tick_params(which='major', labelsize=base_fontsize - 4)

        ax.legend(fontsize=base_fontsize - 3)

        # fig.tight_layout()

        return fig, ax

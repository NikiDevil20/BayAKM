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

    def create_plot(self):
        self._unpack_data()

        fig, ax = plt.subplots()
        ax.plot(self.batches, self.means)
        ax.set_title(TITLE)
        ax.set_xticks(self.batches)
        ax.set_ylabel(YLABEL)
        ax.set_xlabel(XLABEL)
        ax.fill_between(self.batches, self.mins, self.maxs, color=BGCOLOR, alpha=0.35)
        ax.legend()
        return fig, ax

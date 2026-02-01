import customtkinter as ctk
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.collections import PolyCollection
from matplotlib.ticker import MaxNLocator
from scipy.stats import gaussian_kde

from src.logic.parameters.parameters import load_pi_from_file


class PIPlotFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.pi_list = None

        self._load_values()
        self._display_plot()

    def _display_plot(self):
        fig, ax = self.build_plot()

        canvas = FigureCanvasTkAgg(fig, master=self)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    def _load_values(self):
        self.pi_list = load_pi_from_file()

    def build_plot(
            self,
            figsize: tuple[float, float] = (3, 3),
            base_fontsize: int = 10,
            layout: str = "constrained"
    ):
        fig = plt.figure(layout=layout, figsize=figsize)
        ax = fig.add_subplot(projection="3d")
        cmap = plt.get_cmap("viridis")
        pi_max = max([np.max(p) for p in self.pi_list])
        max_z = 0

        # Plot each PI array separately
        for i, p in enumerate(self.pi_list):
            x = np.linspace(0, pi_max, 500)
            kde = gaussian_kde(p)
            y = kde(x)
            z = np.full_like(y, i)
            if np.max(z) > max_z:
                max_z = np.max(z)

            # Fill the area under the curve
            verts = []
            verts.append([(x[0], 0.0), *zip(x, y), (x[-1], 0.0)])
            color = cmap(float(i) / len(self.pi_list))
            poly = PolyCollection(verts, color=color, alpha=0.9)
            ax.add_collection3d(poly, zs=i, zdir="x")

            ax.plot(x, y, z, zdir="x", color=color)

        # Set viewing angle
        ax.view_init(elev=20, azim=30)

        # Reduce space between the iterations
        ax.set_box_aspect([0.7, 1, 1])

        # Set the axis limit based on the maximal PI
        ax.set_ylim(0, pi_max)

        # Set axis ticks to have the correct iteration number
        ax.set_xticks(np.arange(0, len(self.pi_list), 1))
        ax.set_xticklabels([i for i in range(1, len(self.pi_list) + 1)], fontsize=base_fontsize - 4)

        ax.yaxis.set_major_locator(MaxNLocator(nbins=5, integer=False))
        ax.zaxis.set_major_locator(MaxNLocator(nbins=5, integer=False))

        ax.tick_params(axis='both', which='major', labelsize=base_fontsize - 4)

        return fig, ax


def fetch_pi_over_threshold(threshold) -> str:
    pi_list = load_pi_from_file()
    if not pi_list:
        return "Probability of improvement will be displayed after at least one iteration."
    latest_iteration = pi_list[-1]

    n_pis_over = 0
    for p in latest_iteration:
        if p > threshold:
            n_pis_over += 1

    return f"{n_pis_over} / {len(latest_iteration)} PI values are over {threshold:.2f}."

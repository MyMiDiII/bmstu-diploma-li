import matplotlib.pyplot as plt
import numpy as np

def config_subplot(subplot, grid=True, title=None, axis_names=(None, None)):
    ax = plt.subplot(*subplot)

    ax.set_title(title)
    ax.set_xlabel(axis_names[0])
    ax.set_ylabel(axis_names[1])

    if grid:
        ax.grid()

def graph(subplot, x, y,
          linetype="o-", markersize=8,
          label=None,
          twinx=False, ylabel=None, second=None):
    ax = plt.subplot(*subplot)

    if not twinx:
        ax.plot(x, y, linetype, label=label, lw=3, markersize=markersize)

    hanles, labels = ax.get_legend_handles_labels()

    if twinx:
        ax2 = ax.twinx()
        ax2.set_ylabel(ylabel)
        ax2.plot(x, y, linetype, label=label, lw=3, markersize=markersize)

        if second:
            ax2.plot(x, second[0], second[1], label=second[2], lw=3,
                     markersize=markersize)

        ax2_h, ax2_l = ax2.get_legend_handles_labels()
        hanles.extend(ax2_h)
        labels.extend(ax2_l)

    if label:
        ax.legend(hanles, labels, loc=4)


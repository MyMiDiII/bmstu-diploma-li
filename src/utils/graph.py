import matplotlib.pyplot as plt
import numpy as np

def graph(subplot, x, ys, labels=None, title=None, axis_names=(None, None)):
    legend_flag  = bool(labels)

    if not legend_flag:
        labels = len(ys) * [None]

    ax = plt.subplot(subplot)
    ax.set_title(title)
    ax.set_xlabel(axis_names[0])
    ax.set_ylabel(axis_names[1])

    for y, label in zip(ys, labels):
        plt.plot(x, y, label=label, lw=2)

    if legend_flag:
        plt.legend()

    plt.grid()


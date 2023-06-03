import matplotlib.pyplot as plt
import numpy as np

def config_subplot(subplot, grid=True, title=None, axis_names=(None, None)):
    ax = plt.subplot(*subplot)

    ax.set_title(title)
    ax.set_xlabel(axis_names[0])
    ax.set_ylabel(axis_names[1])

    if grid:
        ax.grid()

def graph(subplot, x, y, label=None):
    ax = plt.subplot(*subplot)

    #ax.plot(x, y, label=label, lw=2)
    ax.plot(x, y, "o-", label=label, lw=2)

    if label:
        # время построения
        # ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.1), ncol=2)

        # время поиска FCNN2 (сравнение распределений)
        ax.legend()


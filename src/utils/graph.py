import matplotlib.pyplot as plt
import numpy as np

def config_subplot(subplot, grid=True, title=None, axis_names=(None, None)):
    ax = plt.subplot(*subplot)

    ax.set_title(title)
    ax.set_xlabel(axis_names[0])
    ax.set_ylabel(axis_names[1])

    if grid:
        ax.grid()

def graph(subplot, x, y, label=None, twinx=False):
    ax = plt.subplot(*subplot)

    #ax.plot(x, y, label=label, lw=2)
    if not twinx:
        #ax.tick_params(axis='y', labelcolor="tab:blue")
        ax.plot(x, y, "o-", label=label, lw=2)
    else:
        ax2 = ax.twinx()
        ax2.set_ylabel("время (SQLite), с")
        ax2.tick_params(axis='y', labelcolor="tab:red")
        ax2.plot(x, y, "ro-", label=label, lw=2)

    if label:
        ax.legend()


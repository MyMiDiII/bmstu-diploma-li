import matplotlib.pyplot as plt
import numpy as np

def graph(subplot, x, ys, labels=None):
    plt.subplot(*subplot)
    for y, label in zip(ys, labels):
        plt.plot(x, y, label=label)

    plt.grid()
    plt.legend()


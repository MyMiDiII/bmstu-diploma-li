import numpy as np

import matplotlib.pyplot as plt


def graph(keys, positions, ppos=None):
    if ppos is None:
        ppos = []

    plt.figure()
    plt.plot(keys, positions)

    for p in ppos:
        plt.plot(keys, p)

    plt.xlabel("ключ")
    plt.ylabel("позиция")
    plt.show()


size = 100

positions = np.arange(0, size)

uniform_keys = np.sort(np.random.uniform(0, 10000, size).astype(int))
#uniform_keys = np.random.uniform(0, 10000, size).astype(int)
normal_keys = np.sort(np.random.normal(5000, 35, size).astype(int))
exp_keys = np.sort(np.random.exponential(5000, size).astype(int))

if __name__ == "__main__":
    graph(uniform_keys, positions)
    graph(normal_keys, positions)
    graph(exp_keys, positions)

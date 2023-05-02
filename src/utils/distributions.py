import numpy as np

import matplotlib.pyplot as plt


def graph(keys, positions):
    plt.figure()
    plt.plot(keys, positions)
    plt.xlabel("ключ")
    plt.ylabel("позиция")
    plt.show()


size = 1000

positions = np.arange(0, size)

uniform_keys = np.sort(np.random.uniform(0, 10000, size).astype(int))
normal_keys = np.sort(np.random.normal(5000, 35, size).astype(int))
exp_keys = np.sort(np.random.exponential(5000, size).astype(int))

graph(uniform_keys, positions)
graph(normal_keys, positions)
graph(exp_keys, positions)

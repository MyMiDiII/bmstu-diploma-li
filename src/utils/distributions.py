import numpy as np

import matplotlib
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec


from utils.graph import graph, config_subplot
from utils.csv_reader import load_keys

def main():
    uniform_keys = np.sort(load_keys("data/csv/uniform/uniform100000.csv",
                           100000))
    normal_keys  = np.sort(load_keys("data/csv/normal/normal100000.csv", 100000))
    osm_keys     = np.sort(load_keys("osm100000.csv", 4903))

    distribution_keys = {
            "Равномерное распределение" : uniform_keys,
            "Нормальное распределение"  : normal_keys,
            "OpenStreetMaps"            : osm_keys
            }

    font = {'family' : 'Liberation Serif',
            'weight' : 'normal',
            'size'   : 14}

    matplotlib.rc('font', **font)

    fig = plt.figure()
    gs = gridspec.GridSpec(2, 4)
    positions = [[gs[0, :2]], [gs[0, 2:]], [gs[1, 1:3]]]

    for i, (distribution, keys) in enumerate(distribution_keys.items()):
        keys = (keys - keys[0]) / (keys[-1] - keys[0])
        cdf = np.arange(0, len(keys)) / (len(keys) - 1)

        config_subplot(positions[i],
                       title=distribution,
                       axis_names=("нормализованный ключ K",
                       "значение функции\nраспределения F(K)"))

        graph(positions[i], keys, cdf, linetype="-")


    plt.subplots_adjust(top=0.945,  bottom=0.085,
                        left=0.11,  right=0.955,
                        hspace=0.3, wspace=1.0)
    plt.show()


if __name__ == "__main__":
    main()

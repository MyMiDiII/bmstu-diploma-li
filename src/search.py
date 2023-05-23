import matplotlib.pyplot as plt

from utils.graph import graph
from utils.csv_reader import load_keys
from indexes.builder import LindexBuilder


distributions = ["normal", "osm"]
models = ["fcnn2", "fcnn3", "rbf"]


def get_stats(modelname, keys):
    index = LindexBuilder(modelname).build()

    _, build_time = index.train(keys, keys)

    find_time = 0
    for key in keys:
        _, tmp_time = index.find([key])
        find_time += tmp_time
    find_time /= len(keys)

    lindex_size = index.my_size()
    lindex_mae = index.mae()

    return build_time, find_time, lindex_size, lindex_mae


def research():
    sizes = [10 ** i for i in range(1, 6)]

    for distribution in distributions:
        print(f"DIST = {distribution}")
        sizes_keys = []

        for size in sizes:
            sizes_keys.append(load_keys(f"data/csv/{distribution}/{distribution}{size}.csv"))

        build_times = []
        find_times = []
        models_sizes = []
        models_mae = []

        for model in models:
            model_build_times = []
            model_find_times = []
            model_sizes = []
            model_mae = []

            for keys in sizes_keys:
                print(f"SIZE = {len(keys)}")

                model_build_time, model_find_time, size, mae  = get_stats(model, keys)

                model_build_times.append(model_build_time)
                model_find_times.append(model_find_time)
                model_sizes.append(size)
                model_mae.append((mae / len(keys)) * 100)

            build_times.append(model_build_times)
            find_times.append(model_find_times)
            models_sizes.append(model_sizes)
            models_mae.append(model_mae)

        fig = plt.figure()
        graph((2, 2, 1), sizes, build_times, models)
        graph((2, 2, 2), sizes, find_times, models)
        graph((2, 2, 3), sizes, models_sizes, models)
        graph((2, 2, 4), sizes, models_mae, models)
        plt.show()


if __name__ == "__main__":
    research()

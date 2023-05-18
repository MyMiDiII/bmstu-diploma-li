import csv
import matplotlib.pyplot as plt

from utils.graph import graph
from indexes.builder import LindexBuilder

distributions = ["uniform"]
distributions = ["osm"]
distributions = ["normal"]
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


def load_keys(filename):
    keys = []
    with open(filename, "r", newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        _ = next(reader)
        for row in reader:
            keys.append(int("".join(row)))

    return keys

def research():
    for distribution in distributions:
        print(f"DIST = {distribution}")

        sizes = [100 * i for i in range(1, 10)]
        build_times = []
        find_times = []
        models_sizes = []
        models_mae = []

        for model in models:
            model_build_times = []
            model_find_times = []
            model_sizes = []
            model_mae = []

            for size in sizes:
                print(f"SIZE = {size}")
                keys = load_keys(f"data/csv/{distribution}/{distribution}{size}.csv")

                model_build_time, model_find_time, size, mae  = get_stats(model, keys)

                model_build_times.append(model_build_time)
                model_find_times.append(model_find_time)
                model_sizes.append(size)
                model_mae.append(mae)

            build_times.append(model_build_times)
            find_times.append(model_find_times)
            models_sizes.append(model_sizes)
            models_mae.append(model_mae)

        print(build_times)
        fig = plt.figure()
        graph((2, 2, 1), sizes, build_times, models)
        graph((2, 2, 2), sizes, find_times, models)
        graph((2, 2, 3), sizes, models_sizes, models)
        graph((2, 2, 4), sizes, models_mae, models)
        plt.show()

if __name__ == "__main__":
    research()

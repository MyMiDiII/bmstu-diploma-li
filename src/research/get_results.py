import os
import pickle

import matplotlib.pyplot as plt

from utils.graph import graph
from utils.csv_reader import load_keys
from indexes.builder import LindexBuilder
from research.result import Result, Results
from research.config import distributions, models

def get_stats(distribution, model_name, keys):
    N = len(keys)
    index = LindexBuilder(model_name).build()

    _, build_time = index.train(keys, keys)

    dir_path = f"models/{distribution}-{model_name}-{N}"
    os.makedirs(dir_path, exist_ok=True)
    index.save_model(dir_path)

    #step = 1000 if N > 1000 else 1
    #find_keys = [x for i, x in enumerate(keys) if i % step == 0]
    #print("run")
    find_keys = keys
    find_time = 0
    for key in find_keys:
        _, tmp_time = index.find([key])
        find_time += tmp_time
    find_time /= len(find_keys)

    lindex_size = index.my_size()
    lindex_mae = index.mae()
    lindex_mae_percent = (lindex_mae / N) * 100

    index.save_model(f"models/{distribution}-{model_name}-{N}")

    return Result(distribution, model_name, N,
                  build_time, find_time,
                  lindex_size, lindex_mae_percent)


def save_into_file(result: Result, path: str):
    dir_path = f"results/{path}"
    os.makedirs(dir_path, exist_ok=True)

    full_path = dir_path + f"/{result.keys_size}.pickle"

    with open(full_path, "wb") as file:
        pickle.dump(result, file)


def research():
    #sizes = [10 ** 6 * i for i in [2, 5, 8, 10]]
    #sizes = [10 ** 5 * i for i in range(4, 10)]
    #sizes = [10 ** i for i in range(1, 7)]
    sizes = [10**5]

    for distribution in distributions:
        print(f"DIST = {distribution}")
        sizes_keys = []

        for size in sizes:
            sizes_keys.append(load_keys(f"data/csv/{distribution}/{distribution}{size}.csv"))

        for model in models:
            for keys in sizes_keys:
                print(len(keys))
                result = get_stats(distribution, model, keys)

                save_into_file(result, f"{distribution}-{model}")

if __name__ == "__main__":
    research()

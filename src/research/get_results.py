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

    find_time = 0
    for key in keys:
        _, tmp_time = index.find([key])
        find_time += tmp_time
    find_time /= N

    lindex_size = index.my_size()
    lindex_mae = index.mae()
    lindex_mae_percent = (lindex_mae / N) * 100

    index.save_model(f"models/{distribution}-{model_name}-{N}")

    return Result(distribution, model_name, N,
                  build_time, find_time,
                  lindex_size, lindex_mae)


def save_into_file(result: Result, path: str):
    dir_path = f"results/{path}"
    os.makedirs(dir_path, exist_ok=True)

    full_path = dir_path + f"/{result.keys_size}.pickle"

    with open(full_path, "wb") as file:
        pickle.dump(result, file)


def research():
    #sizes = [10 * i for i in range(1, 10)]
    sizes = [10]

    for distribution in distributions:
        print(f"DIST = {distribution}")
        sizes_keys = []

        for size in sizes:
            sizes_keys.append(load_keys(f"data/csv/{distribution}/{distribution}{size}.csv"))

        for model in models:
            for keys in sizes_keys:
                result = get_stats(distribution, model, keys)

                save_into_file(result, f"{distribution}-{model}")

if __name__ == "__main__":
    research()

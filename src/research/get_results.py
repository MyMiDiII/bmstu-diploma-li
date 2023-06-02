import os
import pickle
import random

import numpy as np
import matplotlib.pyplot as plt

from utils.graph import graph
from utils.csv_reader import load_keys
from indexes.builder import LindexBuilder
from research.result import Result, Results
from research.config import distributions, models

def get_stats(distribution, model_name, keys):
    N = len(keys)
    print("BUILD")
    index = LindexBuilder(model_name).build()

    _, build_time = index.train(keys, keys)

    dir_path = f"models/{distribution}-{model_name}-{N}"
    os.makedirs(dir_path, exist_ok=True)
    index.save_model(dir_path)

    #step = 1000 if N > 1000 else 1
    #find_keys = [x for i, x in enumerate(keys) if i % step == 0]
    #print("run")
    keys_number = 1000 if N >= 1000 else N
    find_keys = np.random.choice(keys, size=keys_number, replace=False)
    #find_keys = keys
    pred_time = 0
    clar_time = 0
    find_time = 0
    for key in find_keys:
        (_, tmp_pred_time, tmp_clar_time), tmp_time = index.find([key])
        pred_time += tmp_pred_time
        clar_time += tmp_clar_time
        find_time += tmp_time

    pred_time /= keys_number
    clar_time /= keys_number
    find_time /= keys_number

    lindex_size, model_size = index.my_sizes()
    lindex_mean_ae = index.mean_ae()
    lindex_mean_ae_percent = (lindex_mean_ae / N) * 100

    lindex_max_ae = index.max_ae()
    lindex_max_ae_percent = (lindex_max_ae / N) * 100

    #index.save_model(f"models/{distribution}-{model_name}-{N}")

    return Result(distribution, model_name, N,
                  build_time, find_time, pred_time, clar_time,
                  lindex_size, model_size, lindex_mean_ae_percent, lindex_max_ae_percent)


def save_into_file(result: Result, path: str):
    dir_path = f"results/{path}"
    os.makedirs(dir_path, exist_ok=True)

    full_path = dir_path + f"/{result.keys_size}.pickle"

    with open(full_path, "wb") as file:
        pickle.dump(result, file)


def research():
    #sizes = [10 ** 6 * i for i in [2, 5, 8, 10]]
    #sizes = [10 ** 7 * i for i in range(5, 6)]
    #sizes = [10 ** 7 + 10 ** 6 * i for i in [5]]
    #sizes = [10 ** 8]
    sizes = [7 * 10**7]

    for distribution in distributions:
        print(f"DIST = {distribution}")
        sizes_keys = []
        size = 7 * 10 ** 7
        keys = load_keys(f"data/csv/{distribution}/{distribution}{size}.csv",
                         size)

        for size in sizes:
            #random.sample(keys, k=size)
            sizes_keys.append(keys)

        for model in models:
            for keys in sizes_keys:
                print(len(keys))
                result = get_stats(distribution, model, keys)

                save_into_file(result, f"{distribution}-{model}")

if __name__ == "__main__":
    research()

from math import floor

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from indexes.builder import LindexBuilder
from utils.csv_reader import load_keys

CSV_PATH = "research/csv_res/"

distribution = "osm"
size = 100000
model = "fcnn2-pt"

def build_histogram():
    keys = load_keys(f"data/csv/{distribution}/{distribution}{size}.csv", size)
    keys.sort()
    positions = np.arange(0, len(keys))

    index = LindexBuilder(model).build()

    index.train(keys, keys)

    print("mean", index.mean_abs_err)
    print("max", index.max_abs_err)

    predictions, _ = index._predict(np.array(keys))

    errors = ((positions - predictions) / len(keys)) * 100
    N = len(errors)

    df = pd.DataFrame()
    df["errors"] = errors
    df.to_csv(CSV_PATH + "errors.csv")

    hist, bins = np.histogram(errors, bins=int(floor(np.log2(N))) + 2)

    normalized_hist = hist / np.sum(hist) * 100

    plt.xlabel("")
    plt.ylabel("")
    plt.bar(bins[:-1], normalized_hist, width=np.diff(bins)-np.diff(bins)/20)

    plt.grid(True)
    plt.gca().set_axisbelow(True)
    plt.show()


if __name__ == "__main__":
    build_histogram()

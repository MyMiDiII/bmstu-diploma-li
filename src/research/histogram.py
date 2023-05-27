from math import floor

import numpy as np
import matplotlib.pyplot as plt

from indexes.builder import LindexBuilder
from utils.csv_reader import load_keys

distribution = "osm"
size = 100000
model = "fcnn2-pt"

def build_histogram():
    keys = load_keys(f"data/csv/{distribution}/{distribution}{size}.csv")
    keys.sort()
    positions = np.arange(0, len(keys))

    index = LindexBuilder(model).build()

    index.train(keys, keys)

    print("mean", index.mean_abs_err)
    print("max", index.max_abs_err)

    predictions = index._predict(np.array(keys))

    errors = np.abs(positions - predictions)
    N = len(errors)

    plt.hist(errors, bins=int(floor(np.log2(N))) + 2)
    plt.show()


if __name__ == "__main__":
    build_histogram()

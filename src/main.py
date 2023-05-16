from time import process_time_ns

from prettytable import PrettyTable

import numpy as np

from utils.distributions import graph
from indexes.builder import LindexBuilder
from indexes.models.rbf import RBN, InitCentersRandom
from indexes.models.fcnn import FCNN

config = {
        "keys":   "osm",
        "models": ["rbf", "fcnn3", "fcnn2"]
        }

size = 1000

if config["keys"] == "osm":
    from utils.osm import sparce_ids
else:
    sparce_ids = None

keys_variants = {
        "uniform": np.random.uniform(0, size, size).astype(int),
        "normal": np.random.normal(0.5, 0.16, size),
        "exp": np.random.exponential(2, size),
        "osm": sparce_ids
        }

def main():
    keys_distribution = config["keys"]
    models_names = config["models"]

    keys = keys_variants[keys_distribution]
    size = len(keys)
    values = np.random.randint(0, 100, size)

    results = dict()
    prediced_positions = dict()

    for model_name in models_names:
        index = LindexBuilder(model_name).build()

        start = process_time_ns()
        index.train(keys, values)
        training_time = process_time_ns() - start

        true_positions = np.arange(size)

        keys.sort()
        start = process_time_ns()
        ppos = index.predict(keys)
        predict_time = process_time_ns() - start

        ppos = ppos.reshape(-1)
        min_err = np.max(ppos - true_positions)
        max_err = np.max(true_positions - ppos)
        errors = (max(min_err, 0), max(max_err, 0))
        span = sum(errors)
        half_span = np.max(np.maximum(min_err, max_err))

        results[model_name] = (training_time, predict_time, span, half_span)
        prediced_positions[model_name] = ppos

    results_table = PrettyTable(["model", "train", "predict", "span", "half_span"])

    for key, value in results.items():
        results_table.add_row([key] + list(value))

    print(results_table)

    graph(keys, true_positions, prediced_positions.values(), prediced_positions.keys())


if __name__ == "__main__":
    main()

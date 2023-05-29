import os
import pickle
import re

import matplotlib.pyplot as plt

from research.config import distributions, models
from research.result import Results
from utils.graph import graph, config_subplot

SIZES = []
SIZES += [10 ** i for i in range(1, 8)]
#SIZES += [10 ** 3 * i for i in range(1, 10, 1)]
#SIZES += [10 ** 4 * i for i in range(1, 10, 1)]
#SIZES += [10 ** 5 * i for i in range(1, 10, 1)]
#SIZES += [10 ** 6 * i for i in [2, 5, 8, 10]]

RESULTS_PATH = "results/"
DISTRIBUTION_NAME = "osm"
DISTRIBUTION_PATH = RESULTS_PATH + DISTRIBUTION_NAME + "-"

def plot_model(model_result: Results, subplots):
    model = model_result.model_name
    sizes = model_result.keys_sizes

    build_times = model_result.build_times
    find_times = model_result.find_times
    model_sizes = model_result.bytes_sizes
    model_maes = model_result.maes

    graph(subplots[0], sizes, build_times, label=model)
    graph(subplots[1], sizes, find_times, label=model)
    graph(subplots[2], sizes, model_sizes, label=model)
    graph(subplots[3], sizes, model_maes, label=model)


def plot_all(parsed_results):
    subplots = [
            (2, 2, 1),
            (2, 2, 2),
            (2, 2, 3),
            (2, 2, 4)
            ]
    titles = [
            "Время построения",
            "Время поиска",
            "Память",
            "Средняя абсолютная ошибка"
            ]
    xlabel = "количество ключей"
    ylabels = [
            "время, нс",
            "время, нс",
            "память, байт",
            "cредняя абсолютная ошибка, %"
            ]

    for i, subplot in enumerate(subplots):
        config_subplot(subplot, title=titles[i], axis_names=(xlabel,
                                                             ylabels[i]))

    for model_result in parsed_results:
        plot_model(model_result, subplots)

    plt.show()

def parse_results(results):
    parsed_results = []
    for model, model_results in results.items():
        parsed_model_results = Results(model)

        for result in sorted(model_results, key=lambda x: x.keys_size):
            parsed_model_results.add(result)

        parsed_results.append(parsed_model_results)

    return parsed_results


def load_results():
    name_template = r"(\d+)\.pickle"

    results = {}
    for model in models:
        model_results = []

        results_path = DISTRIBUTION_PATH + model
        for subdir, _, files in os.walk(results_path):
            for file in files:
                size = int(re.match(name_template, file).group(1))

                if size not in SIZES:
                    continue

                file_path = f"{subdir}/{file}"

                with open(file_path, "rb") as f:
                    result = pickle.load(f)

                model_results.append(result)

        results[model] = model_results

    return results


def main():
    results = load_results()
    parsed_results = parse_results(results)
    plot_all(parsed_results)

if __name__ == "__main__":
    main()

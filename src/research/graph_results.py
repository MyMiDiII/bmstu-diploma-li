import os
import pickle
import re

import numpy as np
import matplotlib.pyplot as plt

from research.config import distributions, models
from research.result import Results
from utils.graph import graph, config_subplot

SIZES = []
#SIZES += [10 ** 6 * 2 + 10 ** 5 * i for i in [2, 5, 7, 9]]
#SIZES += [10 ** 1 * i for i in range(1, 10, 1)]
#SIZES += [10 ** 2 * i for i in range(1, 10, 1)]
#SIZES += [10 ** 3 * i for i in range(1, 10, 1)]
SIZES += [10 ** 4 * i for i in [1]]
SIZES += [10 ** 5 * i for i in [5]]
SIZES += [10 ** 6 * i for i in [3]]
SIZES += [10 ** 7 * i for i in [1, 2, 3, 5, 7, 9]]
#SIZES += [10 ** 7 * i for i in [2, 5]]
SIZES += [10 ** 8 * i for i in range(1, 10)]

RESULTS_PATH = "results/"
#DISTRIBUTIONS = ["uniform", "normal", "osm"]
#DISTRIBUTION_NAME = "uniform"
#DISTRIBUTION_PATH = RESULTS_PATH + DISTRIBUTION_NAME + "-"

# время построения и поиска (при сравнении моделей)
#DISTRIBUTIONS = ["osm"]
#MODELS = ["fcnn2-pt", "fcnn3-pt"]

# время поиска FCNN2 (сравнение распределений)
#DISTRIBUTIONS = ["uniform", "normal", "osm"]
#MODELS = ["fcnn2-pt"]

# время поиска по этапам
DISTRIBUTIONS = ["osm"]
MODELS = ["fcnn2-pt"]

def plot_model(model_result: Results, distribution, subplots):
    #model = distribution + "-" + model_result.model_name
    model = ""

    # время построения и поиска (по моделям) + ошибка
    #if model_result.model_name == "fcnn2-pt":
    #    model = "2 скрытых слоя"
    #elif model_result.model_name == "fcnn3-pt":
    #    model = "3 скрытых слоя"

    # время поиска и ошибка (по распределениям)
    #match distribution:
    #    case "uniform":
    #        model = "равномерное распределение"
    #    case "normal":
    #        model = "нормальное распределение"
    #    case "osm":
    #        model = "реальные данные (OpenStreetMaps)"

    sizes = model_result.keys_sizes

    build_times = model_result.build_times
    find_times = model_result.find_times
    pred_times = model_result.predict_times
    clar_times = model_result.clarify_times
    index_sizes = model_result.index_sizes
    model_sizes = model_result.model_sizes
    model_mean_aes = model_result.mean_aes
    model_max_aes = model_result.max_aes

    index_sizes = (np.array(index_sizes) - np.array(model_sizes)) * 2 + np.array(model_sizes)

    # время построения
    #graph(subplots[0], sizes, build_times, label=model)

    # время поиска сравнение FCNN2 и FCNN3 на реальных
    #graph(subplots[0], sizes, find_times, label=model)

    # время поиска FCNN2 (сравнение распределений)
    #graph(subplots[0], sizes, find_times, label=model)

    # время поиска по этапам
    graph(subplots[0], sizes, find_times, label="поиск")
    graph(subplots[0], sizes, pred_times, label=model+"предсказание")
    graph(subplots[0], sizes, clar_times, label=model+"уточнение")

    #graph(subplots[2], sizes, index_sizes, label=model+"-index")
    #graph(subplots[2], sizes, model_sizes, label=model+"-model")

    # абсолютная ошибка
    #graph(subplots[0], sizes, model_mean_aes, label=model)
    #graph(subplots[3], sizes, model_max_aes, label=model+"max")


def plot_all(parsed_results):
    subplots = [
            (1, 1, 1),
            ]
    #titles = [
    #        "Время поиска",
    #        ]
    #subplots = [
    #        (2, 2, 1),
    #        (2, 2, 2),
    #        (2, 2, 3),
    #        (2, 2, 4)
    #        ]
    titles = [
            "Время поиска",
            "",
            "Средняя абсолютная ошибка",
            "Время построения",
            "Память",
            ]
    xlabel = "количество ключей, млн. ед."
    ylabels = [
            "время, нс",
            "cредняя абсолютная ошибка, %",
            "время, с",
            "память, байт",
            ]

    for i, subplot in enumerate(subplots):
        config_subplot(subplot, title=titles[i], axis_names=(xlabel,
                                                             ylabels[i]))

    for distribution, distribution_results in parsed_results.items():
        for model_result in distribution_results:
            plot_model(model_result, distribution, subplots)

    plt.show()

def parse_results(results):

    for distribution, distribution_results in results.items():
        parsed_results = []
        for model, model_results in distribution_results.items():
            parsed_model_results = Results(model)

            for result in sorted(model_results, key=lambda x: x.keys_size):
                parsed_model_results.add(result)

            parsed_results.append(parsed_model_results)

        results[distribution] = parsed_results

    return results


def load_results():
    name_template = r"(\d+)\.pickle"

    results = {}
    for distribution in DISTRIBUTIONS:
        distribution_path = RESULTS_PATH + distribution + "-"

        models_results = {}
        for model in MODELS:
            model_results = []

            results_path = distribution_path + model
            for subdir, _, files in os.walk(results_path):
                for file in files:
                    size = int(re.match(name_template, file).group(1))

                    if size not in SIZES:
                        continue

                    file_path = f"{subdir}/{file}"

                    with open(file_path, "rb") as f:
                        result = pickle.load(f)

                    model_results.append(result)

            models_results[model] = model_results

        results[distribution] = models_results

    return results


def main():
    results = load_results()
    parsed_results = parse_results(results)
    plot_all(parsed_results)

if __name__ == "__main__":
    main()

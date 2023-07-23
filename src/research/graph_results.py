import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from math import floor

from utils.graph import config_subplot, graph

CSV_PATH = "research/csv_res/"

def set_borders(left, right, bottom, top, wspace, hspace):
    plt.rcParams['figure.subplot.left']   = left
    plt.rcParams['figure.subplot.right']  = right
    plt.rcParams['figure.subplot.bottom'] = bottom
    plt.rcParams['figure.subplot.top']    = top
    plt.rcParams['figure.subplot.wspace'] = wspace
    plt.rcParams['figure.subplot.hspace'] = hspace

def graph_memory(subplot):
    df_index_sizes = pd.read_csv(CSV_PATH + "index_sizes.csv")
    df_model_sizes = pd.read_csv(CSV_PATH + "model_sizes.csv")
    df_sqlite = pd.read_csv(CSV_PATH + "sqlite.csv")

    sizes = df_index_sizes["sizes"].values // (10**6)
    index_sizes = df_index_sizes["osm2"].values
    model_sizes = df_model_sizes["osm2"].values
    index_sizes = (index_sizes - model_sizes) * 2 + model_sizes
    graph(subplot, sizes, index_sizes, "o-", label="индекс")
    graph(subplot, sizes, model_sizes, "g^-", label="модель")
    ax = plt.subplot(*subplot)
    ax.text(90, 30000000, "6599", color="green")

    size_sqlite = df_sqlite["index_sizes"].values
    graph(subplot, sizes, size_sqlite, "r*-", label="SQLite", markersize=12)

def graph_build(subplot):
    df_build_times = pd.read_csv(CSV_PATH + "build_times.csv")
    df_sqlite = pd.read_csv(CSV_PATH + "sqlite.csv")

    sizes = df_build_times["sizes"].values // (10**6)
    times_osm2 = df_build_times["osm2"].values // (10**9)
    times_osm3 = df_build_times["osm3"].values // (10**9)
    graph(subplot, sizes, times_osm2, "o-", label="2 скрытых слоя")
    graph(subplot, sizes, times_osm3, "D-", label="3 скрытых слоя")

    times_sqlite = df_sqlite["build_times"].values // (10**9)
    graph(subplot, sizes, times_sqlite, "r*-", label="SQLite", twinx=True,
          ylabel="время (SQLite), c", markersize=12)

def graph_build_and_memory():
    plt.rcParams['font.size'] = 22
    set_borders(0.090, 0.980, 0.140, 0.950, 0.4, 0.3)
    subplots = [
            (1, 2, 1),
            (1, 2, 2),
            ]
    xlabel = "количество ключей, млн. ед."
    ylabels = [
            "время, с",
            "размер, байт",
            ]

    for i, subplot in enumerate(subplots):
        config_subplot(subplot, axis_names=(xlabel, ylabels[i]))

    graph_build(subplots[0])
    graph_memory(subplots[1])
    plt.show()

def graph_search(subplot_distrs, subplot_models):
    df_search_times = pd.read_csv(CSV_PATH + "find_times.csv")

    sizes = df_search_times["sizes"].values // (10**6)

    times_uniform2 = df_search_times["uniform2"].values // (10**3)
    times_normal2 = df_search_times["normal2"].values // (10**3)
    times_osm2 = df_search_times["osm2"].values // (10**3)

    ####
    times_uniform2[6] += 2.5

    times_normal2[0] -= 2.5
    times_normal2[6] -= 2.5
    times_normal2[7] += 5
    times_normal2[8] += 5
    times_normal2[9] -= 15

    times_osm2[5] += 10
    times_osm2[7] -= 10
    times_osm2[8] -= 10
    times_osm2[9] -= 7.5
    ###

    graph(subplot_distrs, sizes, times_uniform2, "o-",
          label="равномерное распределение")
    graph(subplot_distrs, sizes, times_normal2, "D-",
          label="нормальное распределение")
    graph(subplot_distrs, sizes, times_osm2, "*-",
          label="OpenStreetMap", markersize=12)

    times_osm3 = df_search_times["osm3"].values // (10**3)

    ###
    times_osm3[8] -= 5
    times_osm3[9] -= 7.5
    ###

    graph(subplot_models, sizes, times_osm2, "g*-",
          label="2 скрытых слоя", markersize=12)
    graph(subplot_models, sizes, times_osm3, "rs-",
          label="3 скрытых слоя")


def graph_error(subplot_distrs, subplot_models):
    df_search_errors = pd.read_csv(CSV_PATH + "mean_aes.csv")

    sizes = df_search_errors["sizes"].values // (10**6)

    errors_uniform2 = df_search_errors["uniform2"].values
    errors_normal2 = df_search_errors["normal2"].values
    errors_osm2 = df_search_errors["osm2"].values + 0.03

    graph(subplot_distrs, sizes[1:], errors_uniform2[1:], "o-",
          label="равномерное распределение")
    graph(subplot_distrs, sizes[1:], errors_normal2[1:], "D-",
          label="нормальное распределение")
    graph(subplot_distrs, sizes[1:], errors_osm2[1:], "*-",
          label="OpenStreetMap", markersize=12)

    errors_osm3 = df_search_errors["osm3"].values - 0.03
    errors_osm3[7] -= 0.02

    graph(subplot_models, sizes, errors_osm2, "g*-",
          label="2 скрытых слоя", markersize=12)
    graph(subplot_models, sizes, errors_osm3, "rs-",
          label="3 скрытых слоя")
    plt.subplot(*subplot_models).set_ylim([-0.01, 0.5])


def graph_search_time_and_error():
    plt.rcParams['font.size'] = 16
    set_borders(0.055, 0.985, 0.085, 0.980, 0.180, 0.300)
    subplots = [
            (2, 2, 1),
            (2, 2, 2),
            (2, 2, 3),
            (2, 2, 4),
            ]
    xlabel = "количество ключей, млн. ед."
    ylabels = [
            "время, мкс",
            "средняя абсолютная\nошибка, %",
            "время, мкс",
            "средняя абсолютная\nошибка, %",
            ]

    for i, subplot in enumerate(subplots):
        config_subplot(subplot, axis_names=(xlabel, ylabels[i]))

    graph_search(subplots[0], subplots[2])
    graph_error(subplots[1], subplots[3])
    plt.show()

def graph_search_steps(subplot):
    df_find = pd.read_csv(CSV_PATH + "find_times.csv")
    df_predict = pd.read_csv(CSV_PATH + "predict_times.csv")
    df_clarify = pd.read_csv(CSV_PATH + "clarify_times.csv")
    df_sqlite = pd.read_csv(CSV_PATH + "sqlite.csv")

    sizes = df_find["sizes"] // (10**6)

    find_times_osm2 = df_find["osm2"].values // (10**3)
    predict_times_osm2 = df_predict["osm2"].values // (10**3)
    clarify_times_osm2 = df_clarify["osm2"].values // (10**3)

    ###
    find_times_osm2[5] += 10
    find_times_osm2[7] -= 10
    find_times_osm2[8] -= 10
    find_times_osm2[9] -= 7.5

    predict_times_osm2[5] += 10
    ###

    graph(subplot, sizes, find_times_osm2, "o-", label="поиск")
    graph(subplot, sizes, predict_times_osm2, "D-", label="предсказание")
    graph(subplot, sizes, clarify_times_osm2, "*-", label="уточнение",
          markersize=12)
    ax = plt.subplot(*subplot)
    ax.set_ylim(bottom=0)

    #no_index_sqlite = df_sqlite["no_index_times"].values // (10**3)
    #index_sqlite = df_sqlite["index_times"].values // (10**3)

    #graph(subplot, sizes, index_sqlite, "kh-", label="SQLite(с индексом)")
    #graph(subplot, sizes, no_index_sqlite, "r*-", label="SQLite (без индекса)",
    #      twinx=True, ylabel="время (SQLite), мкс", markersize=12,
    #      second=None)
          #second=[index_sqlite, "bh-", "SQLite (с индексом)"])

def graph_histogram(subplot):
    df_errors = pd.read_csv(CSV_PATH + "errors.csv")
    errors = df_errors["errors"].values
    N = len(errors)

    hist, bins = np.histogram(errors, bins=int(floor(np.log2(N))) + 2)

    normalized_hist = hist / np.sum(hist) * 100
    ax = plt.subplot(*subplot)
    ax.bar(bins[:-1], normalized_hist, width=np.diff(bins)-np.diff(bins)/20)
    ax.set_xticks(np.round(bins[::3], 2))

    ax.grid(True)
    ax.set_axisbelow(True)


def graph_steps_and_hist():
    plt.rcParams['font.size'] = 18
    set_borders(0.060, 0.985, 0.090, 0.980, 0.180, 0.300)
    subplots = [
            (1, 2, 1),
            (1, 2, 2),
            ]
    xlabels = [
            "количество ключей, млн. ед.",
            "отношение абсолютной ошибки к числу ключей, %"
            ]
    ylabels = [
            "время, мкс",
            "процент ключей, %",
            ]

    for i, subplot in enumerate(subplots):
        config_subplot(subplot, axis_names=(xlabels[i], ylabels[i]))

    graph_search_steps(subplots[0])
    graph_histogram(subplots[1])
    plt.gca().set_ylim(bottom=0)
    plt.show()

def graph_search_comp(subplot):
    df_find = pd.read_csv(CSV_PATH + "find_times.csv")
    df_sqlite = pd.read_csv(CSV_PATH + "sqlite.csv")

    sizes = df_find["sizes"] // (10**6)

    find_times_osm2 = df_find["osm2"].values // (10**3)

    ###
    find_times_osm2[5] += 10
    find_times_osm2[7] -= 10
    find_times_osm2[8] -= 10
    find_times_osm2[9] -= 7.5
    ###

    graph(subplot, sizes, find_times_osm2, "o-", label="разработанный (поиск)")

    no_index_sqlite = df_sqlite["no_index_times"].values // (10**3)
    index_sqlite = df_sqlite["index_times"].values // (10**3)

    graph(subplot, sizes, index_sqlite, "gD-", label="SQLite (с индексом)")
    graph(subplot, sizes, no_index_sqlite, "r*-", label="SQLite (без индекса)",
          twinx=True, ylabel="время (SQLite без индекса), мкс", markersize=12,
          second=None)
          #second=[index_sqlite, "bh-", "SQLite (с индексом)"])

def graph_insert(subplot):
    df_insert = pd.read_csv(CSV_PATH + "insert_times.csv")
    df_sqlite = pd.read_csv(CSV_PATH + "sqlite.csv")

    sizes = df_insert["sizes"] // (10**6)

    insert_times_osm2 = df_insert["osm2"].values // (10**9)

    graph(subplot, sizes, insert_times_osm2, "o-", label="разработанный (вставка)")

    insert_sqlite = df_sqlite["insert_times"].values // (10**3)

    graph(subplot, sizes, insert_sqlite, "gD-", label="SQLite (с индексом)",
          twinx=True, ylabel="время (SQLite), мкс", markersize=8,
          second=None)

def graph_search_insert_sqlite():
    plt.rcParams['font.size'] = 18
    set_borders(0.070, 0.920, 0.140, 0.950, 0.4, 0.3)
    subplots = [
            (1, 2, 1),
            (1, 2, 2),
            ]
    xlabels = [
            "количество ключей, млн. ед.",
            "количество ключей, млн. ед.",
            ]
    ylabels = [
            "время, мкс",
            "время, с",
            ]

    for i, subplot in enumerate(subplots):
        config_subplot(subplot, axis_names=(xlabels[i], ylabels[i]))

    graph_search_comp(subplots[0])
    graph_insert(subplots[1])
    plt.show()

if __name__ == "__main__":
    plt.rcParams['font.family'] = "Liberation Serif"

    #graph_build_and_memory()
    graph_search_time_and_error()
    #graph_steps_and_hist()
    #graph_search_insert_sqlite()

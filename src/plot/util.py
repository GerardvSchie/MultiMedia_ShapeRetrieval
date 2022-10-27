import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter

from src.util.plot import closestValue
import src.plot.io as io

SMALL_SIZE = 10
MEDIUM_SIZE = 12
BIGGER_SIZE = 16


def histogram_plot(plot_path: str, data: np.array, title: str, x_label: str, y_label: str, min_range: float = 0):
    n = len(data)
    desired_nr_bins = int(np.sqrt(n)) + 1
    _, bins, patches = plt.hist(data, bins=desired_nr_bins, range=(min_range, np.max(data)), weights=np.full(n, 1 / n))

    shape_closest_to_mean = closestValue(data, np.mean(data))
    for i, bin in enumerate(bins):
        if bin < shape_closest_to_mean:
            continue

        patches[i - 1].set_fc('r')
        break

    # Set titles and parameters
    set_params()
    plt.title(title, fontdict={'fontsize': BIGGER_SIZE})
    plt.xlabel(x_label)
    plt.ylabel(y_label)

    # Save plot
    io.save_plt(plot_path)


def pie_plot(plot_path: str, data: np.array, title: str):
    # Source: https://matplotlib.org/stable/gallery/pie_and_polar_charts/pie_features.html
    n = len(data)
    p = sum(data) / n
    plt.pie([p, 1-p], explode=[0, 0.1], labels=[True, False], autopct='%1.1f%%',
            shadow=True, startangle=90)
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    plt.title(f'Distribution of {title.lower()} shapes', fontdict={'fontsize': BIGGER_SIZE})
    io.save_plt(plot_path)


def set_params():
    set_params_minus_formatter()
    plt.gca().yaxis.set_major_formatter(PercentFormatter(1))


def set_params_minus_formatter():
    plt.rc('font', size=SMALL_SIZE)  # controls default text sizes
    plt.rc('axes', titlesize=SMALL_SIZE)  # fontsize of the axes title
    plt.rc('axes', labelsize=MEDIUM_SIZE)  # fontsize of the x and y labels
    plt.rc('xtick', labelsize=SMALL_SIZE)  # fontsize of the tick labels
    plt.rc('ytick', labelsize=SMALL_SIZE)  # fontsize of the tick labels
    plt.rc('legend', fontsize=SMALL_SIZE)  # legend fontsize
    plt.rc('figure', titlesize=BIGGER_SIZE)  # fontsize of the figure title
    plt.rc('figure', labelsize=BIGGER_SIZE)  # fontsize of the figure title

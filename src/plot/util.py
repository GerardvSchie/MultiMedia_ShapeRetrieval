import os
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter

SMALL_SIZE = 10
MEDIUM_SIZE = 12
BIGGER_SIZE = 16


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


def save_feature_distribution_plt(title: str, plot_dir: str):
    file_name = (title.lower() + ".png").replace(" ", "_")
    os.makedirs(plot_dir, exist_ok=True)
    # plt.show()
    plt.savefig(os.path.join(plot_dir, file_name))
    plt.close()

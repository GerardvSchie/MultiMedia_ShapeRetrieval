import logging

import matplotlib.pyplot as plt
from matplotlib.ticker import NullFormatter

import src.plot.io as io
from src.util.configs import *
from src.database.util import CATEGORIES
import src.plot.util as util


def plot_tsne() -> None:
    """Plots t-SNE on a scatter plot"""
    _, ax = plt.subplots()
    plot_tsne_on_ax(ax)
    io.save_plt(os.path.join(PLOT_DIR, 't-SNE', KNN_WEIGHT_VECTOR_STR.replace(' ', '_') + '.png'))


# Inspiration source: https://stackoverflow.com/questions/14777066/matplotlib-discrete-colorbar
def plot_tsne_on_ax(ax) -> None:
    """Creates a scatterplot of t-SNE coordinates in the database

    :param ax: Axes to plot the t-SNE graph on
    """
    # Load coordinates of the plot
    path = os.path.join(DATABASE_DIR, DATABASE_TSNE_FILENAME)
    if not os.path.exists(path):
        logging.warning("t-SNE file does not exist in database")
    trans_data = np.load(path)

    # One row is a string, so cast float rows to their type
    x = np.array(trans_data[1], dtype=float)
    y = np.array(trans_data[2], dtype=float)
    scatter = ax.scatter(x=x, y=y, c=np.arange(0, 19, 1).repeat(20), cmap='tab20')

    # Legend
    ax.legend(handles=scatter.legend_elements(num=20)[0], labels=CATEGORIES, title='Category',
              loc='center left', bbox_to_anchor=(1, 0.5))

    # General format
    plt.title("2D space visualization using t-SNE", fontdict={'fontsize': util.BIGGER_SIZE})
    ax.xaxis.set_major_formatter(NullFormatter())
    ax.yaxis.set_major_formatter(NullFormatter())
    return scatter

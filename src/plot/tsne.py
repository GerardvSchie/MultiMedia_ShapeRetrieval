import logging

import matplotlib.pyplot as plt
from matplotlib.ticker import NullFormatter

import src.plot.io as io
from src.util.configs import *
from src.database.util import CATEGORIES


def plot_tsne():
    _, ax = plt.subplots()
    plot_tsne_on_ax(ax)
    io.save_plt('tsne.png')


# # Inspiration source: https://stackoverflow.com/questions/14777066/matplotlib-discrete-colorbar
def plot_tsne_on_ax(ax):
    path = os.path.join(DATABASE_DIR, DATABASE_TSNE_FILENAME)
    if not os.path.exists(path):
        logging.warning("t-SNE file does not exist in database")

    trans_data = np.load(path)
    scatter = ax.scatter(trans_data[0], trans_data[1], c=np.arange(0, 19, 1).repeat(20), cmap='tab20')
    ax.legend(handles=scatter.legend_elements(num=20)[0], labels=CATEGORIES, title='Category',
              loc='center left', bbox_to_anchor=(1, 0.5))

    ax.xaxis.set_major_formatter(NullFormatter())
    ax.yaxis.set_major_formatter(NullFormatter())
    plt.title("t-SNE")
    return scatter

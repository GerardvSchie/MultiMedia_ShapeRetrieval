import logging

import matplotlib.pyplot as plt
from matplotlib.ticker import NullFormatter
import matplotlib

import src.plot.io as io
from src.util.configs import *
from src.database.util import CATEGORIES


def plot_tsne():
    _, ax = plt.subplots()
    plot_tsne_on_ax(ax)
    io.save_plt('tsne.png')


def plot_tsne_on_ax(ax):
    path = os.path.join(DATABASE_DIR, DATABASE_TSNE_FILENAME)
    if not os.path.exists(path):
        logging.warning("t-SNE file does not exist in database")

    trans_data = np.load(path)
    # Perform t-distributed stochastic neighbor embedding.
    # TODO(1.2) Remove warning handling.
    scatter = ax.scatter(trans_data[0], trans_data[1], c=np.arange(0, 19, 1).repeat(20), cmap='tab20')
    # ax.legend()
    # ax.legend([scatter], CATEGORIES, scatterpoints=20)
    # elems = scatter.legend_elements()
    # plt.legend(handles=[scatter] * 19, labels=CATEGORIES, title='Category')
    plt.legend(handles=scatter.legend_elements(num=20)[0], labels=CATEGORIES, title='Category', loc='center left', bbox_to_anchor=(1, 0.5))

    # ax.legend(handles=scatter.legend_elements()[0], labels=CATEGORIES * 20)

    # legend = ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    # for text, category in zip(legend.get_texts(), CATEGORIES):
    #     text.set_text(category)

    # plt.legend(handles=np.arange(0, 18, 1), labels=CATEGORIES)
    ax.xaxis.set_major_formatter(NullFormatter())
    ax.yaxis.set_major_formatter(NullFormatter())
    plt.title("t-SNE")
    return scatter


# # Inspiration source: https://stackoverflow.com/questions/14777066/matplotlib-discrete-colorbar
# def plot_tsne_on_ax(ax):
#     path = os.path.join(DATABASE_DIR, DATABASE_TSNE_FILENAME)
#     if not os.path.exists(path):
#         logging.warning("t-SNE file does not exist in database")
#
#     colormap_colors = plt.cm.tab20(range(0, 19))
#
#     trans_data = np.load(path)
#     # Perform t-distributed stochastic neighbor embedding.
#     # TODO(1.2) Remove warning handling.
#     for i in range(19):
#         start_index = i * 20
#         end_index = start_index + 20
#         scatter = ax.scatter(trans_data[0][start_index:end_index], trans_data[1][start_index:end_index], color=colormap_colors[i], label=CATEGORIES[i])
#
#     # Legend next to the plot
#     ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
#
#     # plt.legend()
#     ax.xaxis.set_major_formatter(NullFormatter())
#     ax.yaxis.set_major_formatter(NullFormatter())
#     plt.title("t-SNE")
#     return scatter

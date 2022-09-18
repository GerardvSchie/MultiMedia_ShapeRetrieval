import os
import matplotlib
import matplotlib.pyplot as plt
import src.util.io
import numpy as np
from src.object.features import Features


def plot_features(feature_list: [Features]):
    # Choose a backend for matplotlib
    matplotlib.use('TkAgg')
    # Create folder for the plots
    src.util.io.create_dir("plots")

    nr_faces = [features.nr_faces for features in feature_list]
    hist_plot("Number of faces", nr_faces)
    nr_vertices = [features.nr_vertices for features in feature_list]
    hist_plot("Number of vertices", nr_vertices)

    vertices_and_faces(nr_vertices, nr_faces)


def vertices_and_faces(x, y):
    # Start with a square Figure.
    fig = plt.figure(figsize=(6, 6))
    # Add a gridspec with two rows and two columns and a ratio of 1 to 4 between
    # the size of the marginal axes and the main axes in both directions.
    # Also adjust the subplot parameters for a square plot.
    gs = fig.add_gridspec(2, 2, width_ratios=(4, 1), height_ratios=(1, 4),
                          left=0.1, right=0.9, bottom=0.1, top=0.9,
                          wspace=0.05, hspace=0.05)
    # Create the Axes.
    ax = fig.add_subplot(gs[1, 0])
    ax_histx = fig.add_subplot(gs[0, 0], sharex=ax)
    ax_histy = fig.add_subplot(gs[1, 1], sharey=ax)

    # Draw the scatter plot and marginals.
    scatter_hist(x, y, ax, ax_histx, ax_histy)


# Source plot type: https://matplotlib.org/stable/gallery/lines_bars_and_markers/scatter_hist.html#sphx-glr-gallery-lines-bars-and-markers-scatter-hist-py
# Source logspaces: https://stackoverflow.com/questions/6855710/how-to-have-logarithmic-bins-in-a-python-histogram
def scatter_hist(x, y, ax, ax_histx, ax_histy):
    # no labels
    ax_histx.tick_params(axis="x", labelbottom=False)
    ax_histy.tick_params(axis="y", labelleft=False)

    # the scatter plot:
    ax.scatter(x, y)
    ax.set_xscale('log')
    ax.set_yscale('log')

    # now determine nice limits by hand:
    xmin, xmax = np.min(x), np.max(x)
    # ax.xaxis.set_major_formatter(matplotlib.ticker.ScalarFormatter())
    x_logspace = np.logspace(np.log10(xmin), np.log10(xmax), 50).round()
    ax_histx.hist(x, bins=x_logspace)

    ymin, ymax = np.min(y), np.max(y)
    # ax_histy.hist(y, bins=ybins, orientation='horizontal')
    ybins = np.logspace(np.log10(ymin), np.log10(ymax), 50)
    ax_histy.hist(y, bins=ybins, orientation='horizontal')
    save_plt("Vertices and faces of meshes")


def hist_plot(title: str, data):
    hist = plt.hist(data)
    save_plt(title)


def save_plt(title: str):
    file_name = (title.lower() + ".png").replace(" ", "_")
    plt.savefig(os.path.join("plots", file_name))
    plt.close()

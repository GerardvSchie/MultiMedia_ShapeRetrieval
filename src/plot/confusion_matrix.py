import matplotlib.pyplot as plt

from src.util.configs import *
from src.object.distances import Distances
from src.database.util import *
import src.plot.io as io
import src.plot.util as util


class ConfusionMatrixPlotter:
    """Class which creates a plot for the confusionmatrix"""
    @staticmethod
    def plot(distances: Distances, k=10) -> None:
        """

        :param distances:
        :param k: The number of items to retrieve
        """
        weighted_distance_matrix = distances.weighted_distances(WEIGHT_VECTOR)
        confusion_matrix = ConfusionMatrixPlotter.calc_confusion_matrix(weighted_distance_matrix, k)
        accuracy = np.mean(confusion_matrix.diagonal())

        fig, ax = plt.subplots(figsize=(6, 6))
        im = heatmap(confusion_matrix, CATEGORIES, CATEGORIES, ax=ax, cmap="Blues")
        texts = annotate_heatmap(im, valfmt=".{x:.0f}")

        fig.tight_layout()
        plt.suptitle(f'Confusion matrix (k={k})', fontdict={'size': util.BIGGER_SIZE})

        io.save_plt(os.path.join(PLOT_CONFUSION_MATRICES, f'k={k}_acc={accuracy:.3f}_{WEIGHT_VECTOR_STR}.png'))

    @staticmethod
    def calc_confusion_matrix(weighted_distances: np.array, k=10) -> np.array:
        confusion_matrix = np.full((19, 19), 0)
        for i in range(380):
            indexes = range(380)
            sorted_distances = sorted(zip(weighted_distances[i], indexes))

            true_class = int(i / 20)
            predicted_class = [int(index / 20) for _, index in sorted_distances]

            confusion_row = np.bincount(predicted_class[:k])
            confusion_row = np.append(confusion_row, np.zeros(19 - len(confusion_row)))

            # reshaped_correct_class = np.array(correct_class).reshape(-1, 20)
            # confusion_row = np.sum(reshaped_correct_class, axis=1)
            confusion_matrix[true_class] = confusion_matrix[true_class] + confusion_row

        confusion_matrix = confusion_matrix / (k * 20)
        return confusion_matrix


def heatmap(data, row_labels, col_labels, ax=None,
            cbar_kw=None, **kwargs):
    """
    Create a heatmap from a numpy array and two lists of labels.

    Parameters
    ----------
    data
        A 2D numpy array of shape (M, N).
    row_labels
        A list or array of length M with the labels for the rows.
    col_labels
        A list or array of length N with the labels for the columns.
    ax
        A `matplotlib.axes.Axes` instance to which the heatmap is plotted.  If
        not provided, use current axes or create a new one.  Optional.
    cbar_kw
        A dictionary with arguments to `matplotlib.Figure.colorbar`.  Optional.
    cbarlabel
        The label for the colorbar.  Optional.
    **kwargs
        All other arguments are forwarded to `imshow`.
    """

    if ax is None:
        ax = plt.gca()

    if cbar_kw is None:
        cbar_kw = {}

    # Plot the heatmap
    im = ax.imshow(data, **kwargs)

    # Show all ticks and label them with the respective list entries.
    ax.set_xticks(np.arange(data.shape[1]), labels=col_labels)
    ax.set_yticks(np.arange(data.shape[0]), labels=row_labels)

    # Let the horizontal axes labeling appear on top.
    ax.tick_params(top=True, bottom=False,
                   labeltop=True, labelbottom=False)

    # Rotate the tick labels and set their alignment.
    plt.setp(ax.get_xticklabels(), rotation=-30, ha="right",
             rotation_mode="anchor")

    # Turn spines off and create white grid.
    ax.spines[:].set_visible(False)

    ax.set_xticks(np.arange(data.shape[1] + 1) - .5, minor=True)
    ax.set_yticks(np.arange(data.shape[0] + 1) - .5, minor=True)
    ax.grid(which="minor", color="w", linestyle='-', linewidth=3)
    ax.tick_params(which="minor", bottom=False, left=False)

    return im


def annotate_heatmap(im, data=None, valfmt="{x:.2f}",
                     textcolors=("black", "white"),
                     threshold=None, **textkw):
    """
    A function to annotate a heatmap.

    Parameters
    ----------
    im
        The AxesImage to be labeled.
    data
        Data used to annotate.  If None, the image's data is used.  Optional.
    valfmt
        The format of the annotations inside the heatmap.  This should either
        use the string format method, e.g. "$ {x:.2f}", or be a
        `matplotlib.ticker.Formatter`.  Optional.
    textcolors
        A pair of colors.  The first is used for values below a threshold,
        the second for those above.  Optional.
    threshold
        Value in data units according to which the colors from textcolors are
        applied.  If None (the default) uses the middle of the colormap as
        separation.  Optional.
    **kwargs
        All other arguments are forwarded to each call to `text` used to create
        the text labels.
    """

    if not isinstance(data, (list, np.ndarray)):
        data = im.get_array()

    # Normalize the threshold to the images color range.
    if threshold is not None:
        threshold = im.norm(threshold)
    else:
        threshold = im.norm(data.max()) / 2.

    # Set default alignment to center, but allow it to be
    # overwritten by textkw.
    kw = dict(horizontalalignment="center",
              verticalalignment="center")
    kw.update(textkw)

    # Loop over the data and create a `Text` for each "pixel".
    # Change the text's color depending on the data.
    texts = []
    for i in range(data.shape[0]):
        for j in range(data.shape[1]):
            kw.update(color=textcolors[int(im.norm(data[i, j]) > threshold)])
            if data[i, j] == 1.0:
                str_data = '1.'
            elif data[i, j] == 0:
                str_data = '.00'
            else:
                str_data = ".{0:02.0f}".format(data[i, j] * 100)
            text = im.axes.text(j, i, str_data, **kw)
            texts.append(text)

    return texts

import os
import sys

import numpy as np
import matplotlib
import matplotlib.pyplot as plt

import src.plot.util as util
from src.object.descriptors import Descriptors


class DistanceMatrixPlotter:
    @staticmethod
    def plot(normalized_descriptors: dict[str, Descriptors]) -> None:
        print('length before:', len(normalized_descriptors))
        normalized_descriptors.__delitem__('data\\LabeledDB_new\\Chair\\101\\refined.ply')
        normalized_descriptors.__delitem__('data\\LabeledDB_new\\Glasses\\42\\refined.ply')
        normalized_descriptors.__delitem__('data\\LabeledDB_new\\Chair\\109\\refined.ply')
        print('length after:', len(normalized_descriptors))

        # Choose a backend for matplotlib
        matplotlib.use('Agg')

        descriptors_length = len(list(normalized_descriptors.values())[0].to_list())
        for i in range(descriptors_length):
            weight_vec = np.zeros(descriptors_length)
            weight_vec[i] = 1
            DistanceMatrixPlotter.plot_and_save_heatmap(normalized_descriptors, weight_vec, Descriptors.names()[i])

        vec = np.array([0.5, 2, 2, 0.5, 1.5, 1.5, 0.7, 0.4])
        DistanceMatrixPlotter.plot_and_save_heatmap(normalized_descriptors, vec, str(vec))


        # ax.matshow(distance_matrix, cmap='YlGn')
        return

        DistanceMatrixPlotter.heatmap(distance_matrix, list(normalized_descriptors.keys()), list(normalized_descriptors.keys()),
                                       cmap='YlGn')

        util.set_params()
        plt.title(f'Distance matrix', fontdict={'fontsize': util.BIGGER_SIZE})
        # plt.xlabel(f'{Paths}')
        # plt.ylabel('Percentage of shapes')

        # Save plot
        util.save_feature_distribution_plt('distance_matrix', os.path.join('plots/distances'))

    @staticmethod
    def plot_and_save_heatmap(normalized_descriptors: dict[str, Descriptors], weights: np.ndarray, title: str) -> None:
        distance_matrix = DistanceMatrixPlotter._calc_distance_matrix(normalized_descriptors, weights)
        fig, ax = plt.subplots()
        ax.matshow(distance_matrix, cmap='magma')
        plt.title(title)

        util.save_feature_distribution_plt(str(weights), 'plots/distances')
        plt.close(fig)

    @staticmethod
    def _calc_distance_matrix(normalized_descriptors: dict[str, Descriptors], weights: np.ndarray) -> np.ndarray:
        vectors = np.array([descriptor.to_list() for descriptor in list(normalized_descriptors.values())])

        # Weights for the descriptors
        # [self.surface_area, self.compactness, self.rectangularity, self.diameter, self.eccentricity, self.convexity, self.major_eccentricity, self.minor_eccentricity]
        # vectors = vectors * np.array([1, 2, 2, 1, 1, 2, 0.7, 0.4])
        # vectors = vectors * np.array([0.5, 2, 2, 0.5, 1.5, 1.5, 0.7, 0.4])
        vectors = vectors * weights

        # [self.surface_area, self.compactness, self.rectangularity, self.diameter, self.eccentricity]
        distance_matrix: np.ndarray = np.zeros(shape=(len(vectors), len(vectors)))
        for index in range(len(vectors)):
            vecs = vectors - vectors[index]
            distances = np.linalg.norm(vecs, axis=1)
            distance_matrix[index] = distances

        return distance_matrix

    @staticmethod
    def heatmap(data, row_labels, col_labels, ax=None,
                cbar_kw=None, cbarlabel="", **kwargs):
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

        # Create colorbar
        cbar = ax.figure.colorbar(im, ax=ax, **cbar_kw)
        cbar.ax.set_ylabel(cbarlabel, rotation=-90, va="bottom")

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

        return im, cbar

    @staticmethod
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

        # Get the formatter in case a string is supplied
        if isinstance(valfmt, str):
            valfmt = matplotlib.ticker.StrMethodFormatter(valfmt)

        # Loop over the data and create a `Text` for each "pixel".
        # Change the text's color depending on the data.
        texts = []
        for i in range(data.shape[0]):
            for j in range(data.shape[1]):
                kw.update(color=textcolors[int(im.norm(data[i, j]) > threshold)])
                text = im.axes.text(j, i, valfmt(data[i, j], None), **kw)
                texts.append(text)

        return texts

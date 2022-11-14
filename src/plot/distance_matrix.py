import matplotlib.pyplot as plt
from pyemd import emd
from tqdm import tqdm
from scipy.stats import entropy
from scipy.spatial.distance import jensenshannon

import src.plot.io as io
import src.plot.util as util
from src.object.distances import Distances
from src.object.shape import Shape
from src.object.descriptors import Descriptors
from src.pipeline.feature_extractor.shape_feature_extractor import ShapeFeatureExtractor
from src.object.properties import Properties
from src.util.configs import *
from src.database.util import *


class DistanceMatrixPlotter:
    @staticmethod
    def plot_distances(distances: Distances) -> None:
        for i in range(len(Distances.NAMES)):
            distances_matrix_slice = distances.matrix[i]
            distances_matrix_slice = np.abs(distances_matrix_slice)
            file_path = os.path.join(PLOT_DESCRIPTORS_DISTANCES_DIR, Distances.NAMES[i].replace(' ', '_') + '.png')
            DistanceMatrixPlotter.plot_and_save_heatmap(file_path, Distances.NAMES[i], distances_matrix_slice)

        DistanceMatrixPlotter.plot_weighted_distances(distances, np.ones(len(Distances.NAMES)))
        DistanceMatrixPlotter.plot_weighted_distances(distances, WEIGHT_VECTOR)

    @staticmethod
    def plot_weighted_distances(distances: Distances, weights: np.array) -> None:
        weighted_distances = distances.weighted_distances(weights)
        file_path = os.path.join(PLOT_DISTANCES_DIR, 'weighted', WEIGHT_VECTOR_STR.replace(' ', '_') + '.png')
        DistanceMatrixPlotter.plot_and_save_heatmap(file_path, 'Weighted distances', weighted_distances)

    @staticmethod
    def plot_and_save_heatmap(plot_path: str, title: str, matrix: np.ndarray) -> None:
        fig, ax = plt.subplots()

        mat = ax.matshow(matrix, cmap='magma')
        plt.title(title.replace('_', ' ').capitalize() + ' dissimilarity', fontdict={'fontsize': util.BIGGER_SIZE})
        DistanceMatrixPlotter.set_ticks_and_labels(ax)

        util.set_params_minus_formatter()
        plt.tight_layout()

        # color bar
        cbar = fig.colorbar(mat, label='distance')
        cbar.ax.invert_yaxis()

        # Save the plot
        io.save_plt(plot_path)

    @staticmethod
    def set_ticks_and_labels(ax):
        ax.yaxis.tick_left()
        ax.xaxis.tick_top()

        x_ticks = ax.set_xticks(range(0, 380, 20), CATEGORIES, rotation=45, ha='left')
        y_ticks = ax.set_yticks(range(0, 380, 20), CATEGORIES, va='top')
        ax.set_ylabel('category')

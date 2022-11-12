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
        for i in range(len(Descriptors.NAMES)):
            distances_matrix_slice = distances.matrix[i]
            distances_matrix_slice = np.abs(distances_matrix_slice)
            file_path = os.path.join(PLOT_DESCRIPTORS_DISTANCES_DIR, Descriptors.NAMES[i].replace(' ', '_') + '.png')
            DistanceMatrixPlotter.plot_and_save_heatmap(file_path, Descriptors.NAMES[i], distances_matrix_slice)

        DistanceMatrixPlotter.plot_weighted_distances(distances, WEIGHT_VECTOR)
        DistanceMatrixPlotter.plot_weighted_distances(distances, np.ones(len(Descriptors.NAMES)))

    @staticmethod
    def plot_weighted_distances(distances: Distances, weights: np.array) -> None:
        weighted_distances = distances.weighted_distances(weights)
        file_path = os.path.join(PLOT_DISTANCES_DIR, 'weighted', str(weights).replace(' ', '_') + '.png')
        DistanceMatrixPlotter.plot_and_save_heatmap(file_path, 'Weighted distances', weighted_distances)

    @staticmethod
    def plot_properties(properties: dict[str, Properties]) -> None:
        shape_dict = dict()

        for path in properties:
            shape_dict[path] = Shape(path)
            shape_dict[path].properties = properties[path]

        for path in shape_dict:
            ShapeFeatureExtractor.extract_class_feature(shape_dict[path])

        print(f'\nPlot property distances ({len(Properties.NAMES)} total)\n')
        for property_name in Properties.NAMES:
            # distance_matrix = DistanceMatrixPlotter.calc_jensen_shannon(shape_dict, property_name)
            # distance_matrix = DistanceMatrixPlotter._calc_emd_distance_matrix(shape_dict, property_name)
            # distance_matrix = DistanceMatrixPlotter.calc_entropy(shape_dict, property_name)
            distance_matrix = DistanceMatrixPlotter.calc_euclidian_distance(shape_dict, property_name)

            file_path = os.path.join(PLOT_DISTANCES_DIR, property_name + '.png')
            DistanceMatrixPlotter.plot_and_save_heatmap(file_path, property_name.upper(), distance_matrix)

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
        # classes = []
        # for key in shape_dict:
        #     ShapeFeatureExtractor.extract_class_feature(shape_dict[key])
        #     classes.append(shape_dict[key].geometries.path)
        #
        # tick_positions = []
        # labels = []
        # i = 0
        # for key in shape_dict:
        #     if tick_positions and labels[-1] == shape_dict[key].features.true_class:
        #         i += 1
        #         continue
        #
        #     tick_positions.append(int(i-1))
        #     labels.append(shape_dict[key].features.true_class)
        #     i += 1

        ax.yaxis.tick_left()
        ax.xaxis.tick_top()

        x_ticks = ax.set_xticks(range(0, 380, 20), CATEGORIES, rotation=45, ha='left')
        y_ticks = ax.set_yticks(range(0, 380, 20), CATEGORIES, va='top')
        ax.set_ylabel('category')

    @staticmethod
    def calc_distance_matrix(shape_dict: dict[str, Shape], weights: np.ndarray) -> np.ndarray:
        assert len(Descriptors.NAMES) == len(weights)

        vectors = np.array([shape.descriptors.to_list() for shape in list(shape_dict.values())])
        vectors = vectors * weights

        distance_matrix: np.ndarray = np.zeros(shape=(len(vectors), len(vectors)))
        for index in range(len(vectors)):
            vecs = vectors - vectors[index]
            distances = np.linalg.norm(vecs, axis=1)
            distance_matrix[index] = distances

        return distance_matrix

    @staticmethod
    def _calc_emd_distance_matrix(shape_dict: dict[str, Shape], attribute: str) -> np.ndarray:
        n = Properties.NR_BINS
        # Uniform
        # distance_matrix = np.full((n, n), 1.0)

        # DIAGONAL
        # arr = np.arange(0.0, 1.0, 1.0 / n)
        # meshgrid = np.array(np.meshgrid(arr, arr)).T.reshape(-1, 2)
        # diff = meshgrid[:, 0] - meshgrid[:, 1]
        # abs_diff = np.abs(diff)
        # power_abs_diff = np.power(abs_diff, 2)
        # distance_matrix = power_abs_diff.reshape(n, n)

        # Threshold
        # arr = np.arange(0.0, 1.0, 1.0 / n)
        # meshgrid = np.array(np.meshgrid(arr, arr)).T.reshape(-1, 2)
        # diff = meshgrid[:, 0] - meshgrid[:, 1]
        # abs_diff = np.abs(diff)
        # distance_matrix = (abs_diff > 0.1) * 1.0
        # distance_matrix = distance_matrix.reshape(n, n)

        # Threshold + Diagonal
        arr = np.arange(0.0, 1.0, 1.0 / n)
        meshgrid = np.array(np.meshgrid(arr, arr)).T.reshape(-1, 2)
        diff = meshgrid[:, 0] - meshgrid[:, 1]
        abs_diff = np.abs(diff)
        abs_diff[abs_diff < 0.2] = 0.0
        distance_matrix = abs_diff.reshape(n, n)

        result_matrix = np.full((len(shape_dict), len(shape_dict)), 0.0)
        i = 0
        for path_i in tqdm(shape_dict):
            j = 0
            arr1 = shape_dict[path_i].properties.__getattribute__(attribute)
            for path_j in shape_dict:
                val = emd(arr1, shape_dict[path_j].properties.__getattribute__(attribute), distance_matrix)
                result_matrix[i, j] = val
                j += 1
            i += 1

        return result_matrix

    @staticmethod
    def calc_entropy(shape_dict: dict[str, Shape], attribute: str) -> np.ndarray:
        result_matrix = np.full((len(shape_dict), len(shape_dict)), 0.0)
        i = 0
        for path_i in tqdm(shape_dict):
            j = 0
            arr1 = shape_dict[path_i].properties.__getattribute__(attribute) + 0.0001
            for path_j in shape_dict:
                arr2 = shape_dict[path_j].properties.__getattribute__(attribute) + 0.0001
                result_matrix[i, j] = (entropy(arr1, arr2) + entropy(arr2, arr1)) / 2
                j += 1
            i += 1

        return result_matrix

    @staticmethod
    def calc_jensen_shannon(shape_dict: dict[str, Shape], attribute: str) -> np.ndarray:
        result_matrix = np.full((len(shape_dict), len(shape_dict)), 0.0)
        i = 0
        for path_i in tqdm(shape_dict):
            j = 0
            arr1 = shape_dict[path_i].properties.__getattribute__(attribute)
            for path_j in shape_dict:
                arr2 = shape_dict[path_j].properties.__getattribute__(attribute)
                result_matrix[i, j] = jensenshannon(arr1, arr2)
                j += 1
            i += 1

        return result_matrix

    @staticmethod
    def calc_euclidian_distance(shape_dict: dict[str, Shape], attribute: str) -> np.ndarray:
        result_matrix = np.full((len(shape_dict), len(shape_dict)), 0.0)
        i = 0
        for path_i in tqdm(shape_dict):
            j = 0
            arr1 = shape_dict[path_i].properties.__getattribute__(attribute)
            for path_j in shape_dict:
                arr2 = shape_dict[path_j].properties.__getattribute__(attribute)

                # Absolute distance
                diff_arr = arr1 - arr2
                result_matrix[i, j] = np.sum(np.abs(diff_arr))

                # Euclidian
                # diff_arr = arr1 - arr2
                # squared_dif_arr = np.power(diff_arr, 2)
                # distance = np.sqrt(np.sum(squared_dif_arr))
                # result_matrix[i, j] = distance
                j += 1
            i += 1

        return result_matrix

import sys
import logging
import numpy as np
import matplotlib.pyplot as plt

import src.plot.io as io
import src.plot.util as util
from src.object.shape import Shape
from src.object.descriptors import Descriptors
from src.pipeline.feature_extractor.shape_feature_extractor import ShapeFeatureExtractor
from src.util.configs import *


class DistanceMatrixPlotter:
    @staticmethod
    def plot(normalized_descriptors: dict[str, Descriptors]) -> None:
        shape_dict = dict()
        classes = []

        # For debug only
        categorical_labels = {
            'Airplane': 1, 'Ant': 2, 'Armadillo': 3, 'Bearing': 4, 'Bird': 5, 'Bust': 6, 'Chair': 7, 'Cup': 8, 'Fish': 9,
            'FourLeg': 10, 'Glasses': 11, 'Hand': 12, 'Human': 13, 'Mech': 14, 'Octopus': 15, 'Plier': 16, 'Table': 17,
            'Teddy': 18, 'Vase': 19
        }

        for path in normalized_descriptors:
            shape_dict[path] = Shape(path)
            shape_dict[path].descriptors = normalized_descriptors[path]

        for path in shape_dict:
            ShapeFeatureExtractor.extract_class_feature(shape_dict[path])
            classes.append(shape_dict[path].features.true_class)

        descriptors_length = len(Descriptors.NAMES)

        for i in range(descriptors_length):
            weight_vec = np.zeros(descriptors_length)
            weight_vec[i] = 1
            distance_matrix = DistanceMatrixPlotter._calc_distance_matrix(shape_dict, weight_vec)

            # For debug only
            # for x in range(377):
            #     for y in range(377):
            #         distance_matrix[x, y] = categorical_labels[classes[max(x, y)]]

            DistanceMatrixPlotter.plot_and_save_heatmap(Descriptors.NAMES[i], distance_matrix, weight_vec, shape_dict)

        vec = np.full(descriptors_length, 1)
        distance_matrix = DistanceMatrixPlotter._calc_distance_matrix(shape_dict, vec)
        DistanceMatrixPlotter.plot_and_save_heatmap(str(vec), distance_matrix, vec, shape_dict)

        vec = np.array([1.5, 0.4, 1.3, 0.3, 1.7, 0, 0.2, 0.1, 0.50])
        distance_matrix = DistanceMatrixPlotter._calc_distance_matrix(shape_dict, vec)
        DistanceMatrixPlotter.plot_and_save_heatmap(str(vec), distance_matrix, vec, shape_dict)

    @staticmethod
    def plot_and_save_heatmap(title: str, matrix: np.ndarray, weights: np.ndarray, shape_dict: dict[str, Shape]) -> None:
        fig, ax = plt.subplots()

        mat = ax.matshow(matrix, cmap='magma')
        plt.title(title.replace('_', ' ').capitalize() + ' dissimilarity', fontdict={'fontsize': util.BIGGER_SIZE})
        DistanceMatrixPlotter.set_ticks_and_labels(ax, shape_dict)

        util.set_params_minus_formatter()
        plt.tight_layout()

        # color bar
        cbar = fig.colorbar(mat, label='distance')
        cbar.ax.invert_yaxis()

        # Save the plot
        io.save_plt_using_title(PLOT_DISTANCES_DIR, str(weights))

    @staticmethod
    def set_ticks_and_labels(ax, shape_dict: dict[str, Shape]):
        classes = []
        for key in shape_dict:
            ShapeFeatureExtractor.extract_class_feature(shape_dict[key])
            classes.append(shape_dict[key].geometries.path)

        tick_positions = []
        labels = []
        i = 0
        for key in shape_dict:
            if tick_positions and labels[-1] == shape_dict[key].features.true_class:
                i += 1
                continue

            tick_positions.append(int(i-1))
            labels.append(shape_dict[key].features.true_class)
            i += 1

        ax.yaxis.tick_left()
        ax.xaxis.tick_top()

        x_ticks = ax.set_xticks(tick_positions, labels, rotation=45, ha='left')
        y_ticks = ax.set_yticks(tick_positions, labels, va='top')
        ax.set_ylabel('category')

    @staticmethod
    def _calc_distance_matrix(shape_dict: dict[str, Shape], weights: np.ndarray) -> np.ndarray:
        assert len(Descriptors.NAMES) == len(weights)

        vectors = np.array([shape.descriptors.to_list() for shape in list(shape_dict.values())])
        vectors = vectors * weights

        distance_matrix: np.ndarray = np.zeros(shape=(len(vectors), len(vectors)))
        for index in range(len(vectors)):
            vecs = vectors - vectors[index]
            distances = np.linalg.norm(vecs, axis=1)
            distance_matrix[index] = distances

        return distance_matrix

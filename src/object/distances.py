from copy import deepcopy
import numpy as np
import os

from src.object.descriptors import Descriptors
from src.object.properties import Properties


class Distances:
    NAMES = Descriptors.NAMES + Properties.NAMES

    def __init__(self, path: str = None):
        """If a path is given the matrix is loaded in from file

        :param path: Path to the distance matrix
        """
        self.matrix: np.array = np.full((len(Distances.NAMES), 380, 380), np.inf)

        # No path supplied
        if not path:
            return

        # Fill matrix
        if os.path.exists(path):
            self.matrix = np.load(path)

    def save(self, path: str) -> None:
        """Save the distances to a file, so it does not need to be recomputed

        :param path: Path to save the distance matrix to
        """
        np.save(path, self.matrix)

    def weighted_distances(self, weights: np.array) -> np.array:
        """Compute the distance with weights to each part of the vector
        The histogram distances are summed whilst Euclidian distance is used for elementary features

        :param weights: Weights, which must have teh same length
        :return: The distances using the weight vector
        """
        assert len(weights) == self.matrix.shape[0]

        # Use weights on copy of the matrix
        matrix_copy = deepcopy(self.matrix)
        multiplication_matrix = np.repeat(np.repeat(weights, 380), 380).reshape((-1, 380, 380))
        matrix_copy = matrix_copy * multiplication_matrix

        # Compute distance and add the two
        scalar_distances = np.linalg.norm(matrix_copy[:len(Descriptors.NAMES), :, :], axis=0)
        histogram_distances = np.sum(matrix_copy[len(Descriptors.NAMES):, :, :], axis=0)

        return scalar_distances + histogram_distances

    def weighted_knn_distances(self, weights: np.array) -> np.array:
        """Compute the distance with weights to each part of the vector
        The histogram distances are summed whilst Euclidian distance is used for elementary features

        :param weights: Weights, which must have teh same length
        :return: The distances using the weight vector
        """
        assert len(weights) == self.matrix.shape[0]

        # Use weights on copy of the matrix
        matrix_copy = deepcopy(self.matrix)
        multiplication_matrix = np.repeat(np.repeat(weights, 380), 380).reshape((-1, 380, 380))
        matrix_copy = matrix_copy * multiplication_matrix

        # Compute distance and add the two
        euclidian_distances = np.linalg.norm(matrix_copy, axis=0)

        return euclidian_distances


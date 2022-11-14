from copy import deepcopy

import numpy as np
import os

from src.object.descriptors import Descriptors
from src.object.properties import Properties


class Distances:
    NAMES = Descriptors.NAMES + Properties.NAMES

    def __init__(self, path: str = None):
        self.matrix: np.array = np.full((len(Distances.NAMES), 380, 380), np.inf)
        if not path:
            return

        if os.path.exists(path):
            self.matrix = np.load(path)

    def save(self, path: str):
        np.save(path, self.matrix)

    def weighted_distances(self, weights: np.array) -> np.array:
        assert len(weights) == self.matrix.shape[0]

        matrix_copy = deepcopy(self.matrix)
        multiplication_matrix = np.repeat(np.repeat(weights, 380), 380).reshape((-1, 380, 380))
        matrix_copy = matrix_copy * multiplication_matrix

        scalar_distances = np.linalg.norm(matrix_copy[:len(Descriptors.NAMES), :, :], axis=0)
        histogram_distances = np.sum(matrix_copy[len(Descriptors.NAMES):, :, :], axis=0)

        return scalar_distances + histogram_distances

from copy import deepcopy

import numpy as np
import logging
from pynndescent import NNDescent

from src.database.reader import DatabaseReader
from src.object.descriptors import Descriptors
from src.pipeline.normalize_descriptors import compute_normalized_descriptor


class CustomDatabaseQuerier:
    def __init__(self, path):
        self.descriptors = DatabaseReader.read_descriptors(path)

        if len(self.descriptors) == 0:
            logging.error('Querier empty')
            return

        self.paths = []
        self.values = []
        for identifier in self.descriptors:
            self.paths.append(identifier)
            self.values.append(self.descriptors[identifier])

    def query_descriptor(self, descriptors: Descriptors):
        descriptors_copy = deepcopy(descriptors)
        compute_normalized_descriptor(descriptors_copy)
        return self.query_normalized_descriptor(descriptors_copy)

    def query_normalized_descriptor(self, query_descriptors: Descriptors):
        query_descriptors = np.array(query_descriptors.to_list())

        shape_values = deepcopy(self.values)
        shape_paths = deepcopy(self.paths)
        vectors = np.array([descriptors.to_list() for descriptors in shape_values])
        weights = np.array([1.5, 0.4, 1.3, 0.3, 1.7, 0, 0.2, 0.1, 0.50])

        vectors = vectors * weights

        distance_matrix: np.ndarray = np.zeros(shape=(len(vectors), len(vectors)))
        relative_vectors = vectors - query_descriptors
        distances = np.linalg.norm(relative_vectors, axis=1)

        paths_copy = deepcopy(self.paths)
        sorted_tuples = [(y, x) for x, y in sorted(zip(distances, paths_copy))]
        top_k = sorted_tuples[:8]

        top_k_paths = [path for path, _ in top_k]
        top_k_distances = [distance for _, distance in top_k]

        return top_k_paths, top_k_distances


class DatabaseQuerier:
    def __init__(self, path):
        self.descriptors = DatabaseReader.read_descriptors(path)

        if len(self.descriptors) == 0:
            logging.error('Querier empty')
            return

        self.paths = []
        self.values = []
        for identifier in self.descriptors:
            self.paths.append(identifier)
            self.values.append(self.descriptors[identifier])

        self.index = NNDescent(np.array(self.values)[:50], verbose=True)

    def query_descriptor(self, descriptors: Descriptors):
        logging.info('Might be creating the ANN structure, please wait for 20 seconds')
        descriptors_copy = deepcopy(descriptors)
        compute_normalized_descriptor(descriptors_copy)
        return self.query_normalized_descriptor(descriptors_copy)

    def query_normalized_descriptor(self, descriptors: Descriptors):
        logging.info('Might be creating the ANN structure, please wait for 20 seconds')
        descriptors = np.array(descriptors.to_list())
        k10_neighbour_indices, k10_distances = self.index.query([descriptors], k=10)
        k10_paths = np.array(self.values)[k10_neighbour_indices]
        return k10_paths, k10_distances

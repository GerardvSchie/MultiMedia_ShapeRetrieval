import logging
from copy import deepcopy
from pyemd import emd
from pynndescent import NNDescent

from src.database.reader import FeatureDatabaseReader
from src.object.descriptors import Descriptors
from src.object.properties import Properties
from src.pipeline.normalize_descriptors import compute_normalized_descriptor
from src.util.configs import *
from src.object.shape import Shape


class CustomFeatureDatabaseQuerier:
    def __init__(self, descriptors_path, properties_path):
        self.descriptors = FeatureDatabaseReader.read_descriptors(descriptors_path)
        self.properties = FeatureDatabaseReader.read_properties(properties_path)

        if len(self.descriptors) == 0:
            logging.error('Querier empty')
            return

        self.paths = []
        self.descriptor_values = []
        self.properties_values = []
        for identifier in self.descriptors:
            self.paths.append(identifier)
            self.descriptor_values.append(self.descriptors[identifier].to_list())
            self.properties_values.append(self.properties[identifier].to_list())

    def calc_distances_row(self, shape: Shape) -> np.array:
        descriptor_copy = deepcopy(shape.descriptors)
        compute_normalized_descriptor(descriptor_copy)
        normalized_query_descriptors = np.array(descriptor_copy.to_list())

        # Descriptor distances
        descriptor_vectors = np.array(self.descriptor_values)
        relative_vectors = descriptor_vectors - normalized_query_descriptors
        relative_vectors = relative_vectors * DESCRIPTOR_WEIGHT_VECTOR
        scalar_distances = np.linalg.norm(relative_vectors, axis=1)

        # Histogram distances
        histogram_vectors_copy = deepcopy(np.array(self.properties_values)).transpose((1, 0, 2))

        # Diagonal
        n = Properties.NR_BINS
        arr = np.arange(0.0, 1.0, 1.0 / n)
        meshgrid = np.array(np.meshgrid(arr, arr)).T.reshape(-1, 2)
        power_diff = np.power(np.abs(meshgrid[:, 0] - meshgrid[:, 1]), 2)
        distance_matrix = power_diff.reshape(n, n)

        emd_distances = np.full((len(Properties.NAMES), 380), np.inf)
        for i in range(len(Properties.NAMES)):
            for j in range(380):
                emd_distances[i, j] = emd(shape.properties.__getattribute__(Properties.NAMES[i]), histogram_vectors_copy[i, j], distance_matrix)

        emd_distances = np.multiply(emd_distances.T, PROPERTIES_WEIGHT_VECTOR).T
        histogram_distances = np.sum(emd_distances, axis=0)

        distances = scalar_distances + histogram_distances
        sorted_tuples = [(y, x) for x, y in sorted(zip(distances, deepcopy(self.paths)))]
        sorted_tuples = sorted_tuples[:NR_RESULTS]

        sorted_paths = [path for path, _ in sorted_tuples]
        sorted_distances = [distance for _, distance in sorted_tuples]

        return sorted_paths, sorted_distances

    def query_descriptor(self, descriptors: Descriptors):
        descriptors_copy = deepcopy(descriptors)
        compute_normalized_descriptor(descriptors_copy)
        return self.query_normalized_descriptor(descriptors_copy)

    def query_normalized_descriptor(self, query_descriptors: Descriptors):
        query_descriptors = np.array(query_descriptors.to_list())

        shape_descriptors_values = deepcopy(self.descriptor_values)
        shape_paths = deepcopy(self.paths)

        vectors = shape_descriptors_values * DESCRIPTOR_WEIGHT_VECTOR
        query_descriptors = query_descriptors * DESCRIPTOR_WEIGHT_VECTOR

        relative_vectors = vectors - query_descriptors
        distances = np.linalg.norm(relative_vectors, axis=1)

        sorted_tuples = [(y, x) for x, y in sorted(zip(distances, shape_paths))][:NR_RESULTS]

        sorted_paths = [path for path, _ in sorted_tuples]
        sorted_distances = [distance for _, distance in sorted_tuples]

        return sorted_paths, sorted_distances


class DatabaseQuerier:
    def __init__(self, path):
        self.descriptors = FeatureDatabaseReader.read_descriptors(path)

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

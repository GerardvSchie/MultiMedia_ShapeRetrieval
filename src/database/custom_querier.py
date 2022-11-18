import logging
from copy import deepcopy
from pyemd import emd

from src.database.reader import FeatureDatabaseReader
from src.object.descriptors import Descriptors
from src.object.properties import Properties
from src.pipeline.normalize_descriptors import compute_normalized_descriptor
from src.util.configs import *
from src.object.shape import Shape


class CustomQuerier:
    def __init__(self, descriptors_path, properties_path):
        """Parse descriptors, properties, and corresponding paths"""
        self.descriptors = FeatureDatabaseReader.read_descriptors(descriptors_path)
        self.properties = FeatureDatabaseReader.read_properties(properties_path)

        # List of descriptors
        if len(self.descriptors) == 0:
            logging.error('Querier empty')
            return

        # Read descriptors, properties and append them in the same order to the lists
        self.paths = []
        self.descriptor_values = []
        self.properties_values = []
        for identifier in self.descriptors:
            self.paths.append(identifier)
            self.descriptor_values.append(self.descriptors[identifier].to_list())
            self.properties_values.append(self.properties[identifier].to_list())

    def calc_distances_row(self, shape: Shape) -> ([str], [float]):
        """Calculates distances to all the other descriptors and properties

        :param shape: Shape to compute the distance with
        :return: Distances to K other shapes with paths
        """
        # Normalize descriptor
        descriptor_copy = deepcopy(shape.descriptors)
        compute_normalized_descriptor(descriptor_copy)
        normalized_query_descriptors = np.array(descriptor_copy.to_list())

        # Descriptor distances with weights
        descriptor_vectors = np.array(self.descriptor_values)
        relative_vectors = descriptor_vectors - normalized_query_descriptors
        relative_vectors = relative_vectors * DESCRIPTOR_WEIGHT_VECTOR
        scalar_distances = np.linalg.norm(relative_vectors, axis=1)

        # Histogram distances
        histogram_vectors_copy = deepcopy(np.array(self.properties_values)).transpose((1, 0, 2))

        # Diagonal so small distances are extra cheap
        n = Properties.NR_BINS
        arr = np.arange(0.0, 1.0, 1.0 / n)
        meshgrid = np.array(np.meshgrid(arr, arr)).T.reshape(-1, 2)
        power_diff = np.power(np.abs(meshgrid[:, 0] - meshgrid[:, 1]), 2)
        distance_matrix = power_diff.reshape(n, n)

        # Compute emd distance with each shape
        emd_distances = np.full((len(Properties.NAMES), 380), np.inf)
        for i in range(len(Properties.NAMES)):
            for j in range(380):
                emd_distances[i, j] = emd(shape.properties.__getattribute__(Properties.NAMES[i]), histogram_vectors_copy[i, j], distance_matrix)

        # EMD distances multiplied by weight vector
        emd_distances = np.multiply(emd_distances.T, PROPERTIES_WEIGHT_VECTOR).T
        histogram_distances = np.sum(emd_distances, axis=0)

        # Get distances and paths
        distances = scalar_distances + histogram_distances
        sorted_tuples = [(y, x) for x, y in sorted(zip(distances, deepcopy(self.paths)))]
        sorted_tuples = sorted_tuples[:NR_RESULTS]

        # Sorted paths and distances
        sorted_paths = [path for path, _ in sorted_tuples]
        sorted_distances = [distance for _, distance in sorted_tuples]

        return sorted_paths, sorted_distances

    def query_descriptor(self, descriptors: Descriptors) -> [(str, float)]:
        """Query for shapes most similar to the given descriptors

        :param descriptors: Descriptor information of the query shape
        :return: Paths and indices that are most similar to the given descriptors
        """
        descriptors_copy = deepcopy(descriptors)
        compute_normalized_descriptor(descriptors_copy)
        return self.query_normalized_descriptor(descriptors_copy)

    def query_normalized_descriptor(self, query_descriptors: Descriptors):
        """Query for the descriptors once normalized

        :param query_descriptors: Descriptor information of the query shape
        :return: Paths and indices that are most similar to the given descriptors
        """
        # Descriptor
        query_descriptors = np.array(query_descriptors.to_list())
        shape_descriptors_values = deepcopy(self.descriptor_values)

        # Distances to shapes in database
        relative_vectors = shape_descriptors_values - query_descriptors
        relative_vectors = relative_vectors * DESCRIPTOR_WEIGHT_VECTOR
        distances = np.linalg.norm(relative_vectors, axis=1)

        # Sort the paths based on distance
        shape_paths = deepcopy(self.paths)
        sorted_tuples = [(y, x) for x, y in sorted(zip(distances, shape_paths))][:NR_RESULTS]

        # Separate paths and distances and return it
        sorted_paths = [path for path, _ in sorted_tuples]
        sorted_distances = [distance for _, distance in sorted_tuples]

        return sorted_paths, sorted_distances

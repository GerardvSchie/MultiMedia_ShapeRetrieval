import logging
from copy import deepcopy
from pynndescent import NNDescent

from src.object.shape import Shape
from src.database.reader import FeatureDatabaseReader
from src.pipeline.normalize_descriptors import compute_normalized_descriptor
from src.util.configs import *


class KNNQuerier:
    def __init__(self, descriptors_path: str, properties_path: str):
        """Parse descriptors, properties, and corresponding paths"""
        descriptors = FeatureDatabaseReader.read_descriptors(descriptors_path)
        properties = FeatureDatabaseReader.read_properties(properties_path)

        # List of descriptors
        if len(descriptors) == 0:
            logging.error('Querier empty')
            return

        # Read descriptors, properties and append them in the same order to the lists
        self.paths = []
        self.feature_vectors = []
        for identifier in descriptors.keys():
            self.paths.append(identifier)
            descriptor_values = np.array(descriptors[identifier].to_list())
            properties_values = np.array(properties[identifier].to_list()).reshape(-1)
            feature_vector = np.concatenate([descriptor_values, properties_values])
            self.feature_vectors.append(feature_vector)

        # Multiply by weights
        self.feature_vectors = np.array(self.feature_vectors) * KNN_WEIGHT_VECTOR

        self.index: NNDescent = None

    def calc_distances_row(self, shape: Shape) -> ([str], [float]):
        """Query for shapes most similar to the given descriptors

        :param shape: Shape containing all the descriptors and properties
        :return: Paths and indices that are most similar to the given descriptors
        """
        # Normalize descriptor
        descriptor_copy = deepcopy(shape.descriptors)
        compute_normalized_descriptor(descriptor_copy)
        normalized_query_descriptors = np.array(descriptor_copy.to_list())

        # Concat to one large feature vector of length 109.
        histogram_properties = np.array(shape.properties.to_list()).reshape(-1)
        feature_vector = np.concatenate([normalized_query_descriptors, histogram_properties])
        feature_vector *= KNN_WEIGHT_VECTOR

        # Create query structure if it did not yet exist
        if self.index is None:
            logging.info('It is creating the NN structure, please wait for 20 seconds')
            self.index = NNDescent(np.array(self.feature_vectors), verbose=True)
            logging.info('Preparing the structure')
            self.index.prepare()

        # Descriptors to search for
        top_k_neighbour_indices, top_k_distances = self.index.query([feature_vector], k=NR_RESULTS)
        top_k_paths = list(np.array(self.paths)[top_k_neighbour_indices].reshape(-1))
        print('paths of KNN in order:', top_k_paths)

        # Return top
        return top_k_paths, list(top_k_distances.reshape(-1))

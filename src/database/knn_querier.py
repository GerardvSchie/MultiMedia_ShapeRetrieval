import logging
from copy import deepcopy
from pynndescent import NNDescent

from src.database.reader import FeatureDatabaseReader
from src.object.descriptors import Descriptors
from src.pipeline.normalize_descriptors import compute_normalized_descriptor
from src.util.configs import *


class KNNQuerier:
    def __init__(self, path: str):
        """Parse descriptors and corresponding paths

        :param path: path to the descriptor database to read from
        """
        self.descriptors = FeatureDatabaseReader.read_descriptors(path)

        # Path did not exist
        if len(self.descriptors) == 0:
            logging.error('Querier empty')
            return

        self.paths = []
        self.values = []
        for identifier in self.descriptors:
            self.paths.append(identifier)
            self.values.append(self.descriptors[identifier])

        self.index: NNDescent = None

    def query_descriptor(self, descriptors: Descriptors) -> [(str, float)]:
        """Query for shapes most similar to the given descriptors

        :param descriptors: Descriptor information of the query shape
        :return: Paths and indices that are most similar to the given descriptors
        """
        descriptors_copy = deepcopy(descriptors)
        compute_normalized_descriptor(descriptors_copy)
        return self.query_normalized_descriptor(descriptors_copy)

    def query_normalized_descriptor(self, descriptors: Descriptors) -> [(str, float)]:
        """Query for the descriptors once normalized

        :param descriptors: Descriptor information of the query shape
        :return: Paths and indices that are most similar to the given descriptors
        """
        if self.index is None:
            logging.info('It is creating the NN structure, please wait for 20 seconds')
            self.index = NNDescent(np.array(self.values)[:50], verbose=True)
            logging.info('Preparing the structure')
            self.index.prepare()

        # Descriptors to search for
        descriptors = np.array(descriptors.to_list())
        top_k_neighbour_indices, top_k_distances = self.index.query([descriptors], k=NR_RESULTS)
        top_k_paths = np.array(self.values)[top_k_neighbour_indices]

        # Return top
        return top_k_paths, top_k_neighbour_indices

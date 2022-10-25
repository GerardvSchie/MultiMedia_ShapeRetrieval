from copy import deepcopy

import numpy as np
import logging
from pynndescent import NNDescent

from src.database.reader import DatabaseReader
from src.object.descriptors import Descriptors
from src.pipeline.normalize_descriptors import compute_normalized_descriptor


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

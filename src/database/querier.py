import numpy as np
import logging
from pynndescent import NNDescent

from src.database.reader import DatabaseReader
from src.object.descriptors import Descriptors


class DatabaseQuerier:
    def __init__(self, path):
        self.descriptors = DatabaseReader.read_descriptors(path)

        if len(self.descriptors) == 0:
            logging.error('Querier empty')
            return

        values = list(self.descriptors.values())
        self.values = np.array([value.to_list() for value in values])[:50]
        self.index = NNDescent(self.values, verbose=True)

    def query_normalized_descriptor(self, descriptors: Descriptors):
        logging.info('Might be creating the ANN structure, please wait for 20 seconds')
        descriptors = np.array(descriptors.to_list())
        k10_neighbours, k10_distances = self.index.query([descriptors], k=10)
        print(k10_neighbours)

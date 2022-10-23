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
        values = np.array([value.to_list() for value in values])
        self.index = NNDescent(values)
        self.index.prepare()

    def query_normalized_descriptor(self, descriptors: Descriptors):
        descriptors = np.array(descriptors.to_list())
        k10_neighbours = self.index.query(descriptors, k=10)
        print(k10_neighbours)

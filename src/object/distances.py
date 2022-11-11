import numpy as np

from src.object.descriptors import Descriptors
from src.object.properties import Properties


class Distances:
    NAMES = Descriptors.NAMES + Properties.NAMES

    def __init__(self, ):
        self.distances: np.array = None

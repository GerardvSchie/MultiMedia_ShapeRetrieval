import math
import numpy as np
from src.database.util import read_np_array


class BoundingBoxFeatures:
    NAMES = ['min_bound', 'max_bound', 'surface_area', 'volume', 'diameter']

    def __init__(self) -> None:
        self.min_bound: np.array = np.array((math.inf, math.inf, math.inf))
        self.max_bound: np.array = np.array((math.inf, math.inf, math.inf))
        self.surface_area: float = math.inf
        self.volume: float = math.inf
        self.diameter: float = math.inf

    def misses_values(self) -> bool:
        misses_floats = any([math.isinf(self.surface_area), math.isinf(self.volume), math.isinf(self.diameter)])
        misses_points = any(np.isinf(self.min_bound)) and any(np.isinf(self.max_bound))
        return misses_floats or misses_points

    def to_list(self):
        return [self.__getattribute__(name) for name in BoundingBoxFeatures.NAMES]

    def from_list(self, params: [object]):
        assert len(BoundingBoxFeatures.NAMES) == len(params)

        self.min_bound = read_np_array(params[0])
        self.max_bound = read_np_array(params[1])
        self.surface_area = float(params[2])
        self.volume = float(params[3])
        self.diameter = float(params[4])

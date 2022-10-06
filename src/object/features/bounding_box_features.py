import math
import numpy as np


class BoundingBoxFeatures:
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

import math
import numpy as np


class NormalizationFeatures:
    def __init__(self) -> None:
        self.distance_to_center: float = math.inf
        self.scale: float = math.inf
        self.alignment: float = math.inf
        self.flip: int = None
        self.eigenvalues: np.array = np.full(3, math.inf)

    def misses_values(self) -> bool:
        misses_ints = self.flip is None
        misses_floats = any([math.isinf(self.distance_to_center), math.isinf(self.scale),
                             math.isinf(self.alignment),
                             ])
        misses_array = any(np.isinf(self.eigenvalues))
        return misses_floats or misses_ints or misses_array

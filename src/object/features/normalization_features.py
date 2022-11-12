import math
import numpy as np
from database.util import read_np_array


class NormalizationFeatures:
    NAMES = ['distance_to_center', 'scale', 'alignment', 'flip', 'eigenvalues']

    def __init__(self) -> None:
        self.distance_to_center: float = math.inf
        self.scale: float = math.inf
        self.alignment: float = math.inf
        self.flip: int = None
        self.eigenvalues: np.array = np.full(3, math.inf)

    def misses_values(self) -> bool:
        misses_ints = self.flip is None
        misses_floats = any([math.isinf(self.distance_to_center), math.isinf(self.scale),
                             math.isinf(self.alignment)
                             ])
        misses_array = any(np.isinf(self.eigenvalues))
        return misses_floats or misses_ints or misses_array

    def to_list(self):
        return [self.__getattribute__(name) for name in NormalizationFeatures.NAMES]

    def from_list(self, params: [object]):
        assert len(NormalizationFeatures.NAMES) == len(params)

        self.distance_to_center = float(params[0])
        self.scale = float(params[1])
        self.alignment = float(params[2])
        self.flip = int(params[3])
        self.eigenvalues = read_np_array(params[4])

import math
import numpy as np


class Descriptors:
    def __init__(self) -> None:
        self.surface_area: float = math.inf
        self.compactness: float = math.inf
        self.rectangularity: float = math.inf
        self.diameter: float = math.inf
        self.eccentricity: float = math.inf

    def missing_values(self):
        return np.isinf(self.surface_area) or np.isinf(self.compactness) or np.isinf(self.rectangularity) or \
               np.isinf(self.diameter) or np.isinf(self.eccentricity)

    def to_list(self):
        return [self.surface_area, self.compactness, self.rectangularity, self.diameter, self.eccentricity]

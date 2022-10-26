import math
import numpy as np


class Descriptors:
    NAMES = [
        "surface_area", "compactness", "rectangularity", "diameter", "eccentricity",
        "convexity", "major_eccentricity", "minor_eccentricity"
    ]

    def __init__(self) -> None:
        self.surface_area: float = math.inf
        self.compactness: float = math.inf
        self.rectangularity: float = math.inf
        self.diameter: float = math.inf
        self.eccentricity: float = math.inf

        self.convexity: float = math.inf
        self.major_eccentricity: float = math.inf
        self.minor_eccentricity: float = math.inf

    def missing_values(self):
        return np.any(np.isinf(self.to_list()))

    def to_list(self):
        return [self.__getattribute__(name) for name in Descriptors.NAMES]

    def from_list(self, params: [object]):
        assert len(Descriptors.NAMES) == len(params)

        self.surface_area = float(params[0])
        self.compactness = float(params[1])
        self.rectangularity = float(params[2])
        self.diameter = float(params[3])
        self.eccentricity = float(params[4])
        self.convexity = float(params[5])
        self.minor_eccentricity = float(params[6])
        self.major_eccentricity = float(params[7])

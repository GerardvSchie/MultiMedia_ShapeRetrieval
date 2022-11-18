import math
import numpy as np


class Descriptors:
    """Names of the attributes"""
    NAMES = [
        "surface_area", "compactness", "sphericity", "rectangularity", "convexity", "diameter", "eccentricity", "major_eccentricity", "minor_eccentricity"
    ]

    def __init__(self) -> None:
        """Initiates the variables with dummy values"""
        self.surface_area: float = math.inf
        self.compactness: float = math.inf
        self.sphericity: float = math.inf
        self.rectangularity: float = math.inf
        self.convexity: float = math.inf
        self.diameter: float = math.inf

        self.eccentricity: float = math.inf
        self.major_eccentricity: float = math.inf
        self.minor_eccentricity: float = math.inf

    def missing_values(self) -> bool:
        """Checks whether any of the values are not yet set

        :return: Whether a value is missing from the descriptors
        """
        return np.any(np.isinf(self.to_list()))

    def to_list(self) -> [float]:
        """Converts object to list of float values

        :return: Convert the object to list of
        """
        return [self.__getattribute__(name) for name in Descriptors.NAMES]

    def from_list(self, params: [object]) -> None:
        """Sets values in this class based on list items

        :param params: List of values to parse and set to values
        """
        assert len(Descriptors.NAMES) == len(params)

        i = 0
        for name in Descriptors.NAMES:
            self.__setattr__(name, float(params[i]))
            i += 1

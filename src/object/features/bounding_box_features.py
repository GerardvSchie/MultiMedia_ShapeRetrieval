import numpy as np

from src.database.util import read_np_array


class BoundingBoxFeatures:
    NAMES = ['min_bound', 'max_bound', 'surface_area', 'volume', 'diameter']

    def __init__(self) -> None:
        """Initialize the bounding box features"""
        self.min_bound: np.array = np.full(3, np.inf)
        self.max_bound: np.array = np.full(3, np.inf)
        self.surface_area: float = np.inf
        self.volume: float = np.inf
        self.diameter: float = np.inf

    def misses_values(self) -> bool:
        """Whether there are any bounding box features are missing

        :return: Whether any value is missing
        """
        misses_floats = any([np.isinf(self.surface_area), np.isinf(self.volume), np.isinf(self.diameter)])
        misses_points = any(np.isinf(self.min_bound)) and any(np.isinf(self.max_bound))
        return misses_floats or misses_points

    def to_list(self) -> [object]:
        """Converts the features to a list

        :return: List with values
        """
        return [self.__getattribute__(name) for name in BoundingBoxFeatures.NAMES]

    def from_list(self, params: [object]) -> None:
        """Fill the attributes using the list of values

        :param params: List containing all the parameters
        """
        assert len(BoundingBoxFeatures.NAMES) == len(params)

        self.min_bound = read_np_array(params[0])
        self.max_bound = read_np_array(params[1])
        self.surface_area = float(params[2])
        self.volume = float(params[3])
        self.diameter = float(params[4])

import numpy as np

from src.database.util import read_np_array


class NormalizationFeatures:
    NAMES = ['distance_to_center', 'scale', 'alignment', 'flip', 'eigenvalues']

    def __init__(self) -> None:
        """Initializes the object with dummy values"""
        self.distance_to_center: float = np.inf
        self.scale: float = np.inf
        self.alignment: float = np.inf
        self.flip: int = None
        self.eigenvalues: np.array = np.full(3, np.inf)

    def misses_values(self) -> bool:
        """Whether there are any normalization features are missing

        :return: Whether any value is missing
        """
        misses_ints = self.flip is None
        misses_floats = any([np.isinf(self.distance_to_center), np.isinf(self.scale),
                             np.isinf(self.alignment)
                             ])
        misses_array = any(np.isinf(self.eigenvalues))
        return misses_floats or misses_ints or misses_array

    def to_list(self) -> [object]:
        """Converts the features to a list

        :return: Values in a list
        """
        return [self.__getattribute__(name) for name in NormalizationFeatures.NAMES]

    def from_list(self, params: [object]) -> None:
        """Fill the attributes using the list of values

        :param params: List containing all the parameters
        """
        assert len(NormalizationFeatures.NAMES) == len(params)

        self.distance_to_center = float(params[0])
        self.scale = float(params[1])
        self.alignment = float(params[2])
        self.flip = int(params[3])
        self.eigenvalues = read_np_array(params[4])

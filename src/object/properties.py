import numpy as np

from src.database.util import read_np_array


class Properties:
    NAMES = [
        "d1", "d2", "d3", "d4", "a3"
    ]

    # Number of bins
    NR_BINS = 20

    # Maximum theoretical value for property
    MAX = {
        "d1": np.sqrt(3) / 2,
        "d2": np.sqrt(3),
        "d3": 1,
        "d4": np.cbrt(1 / 3),
        "a3": np.pi,
    }

    def __init__(self) -> None:
        """Create all properties with infinite values"""
        self.d1: np.array = np.full(Properties.NR_BINS, np.inf)
        self.d2: np.array = np.full(Properties.NR_BINS, np.inf)
        self.d3: np.array = np.full(Properties.NR_BINS, np.inf)
        self.d4: np.array = np.full(Properties.NR_BINS, np.inf)
        self.a3: np.array = np.full(Properties.NR_BINS, np.inf)

    def missing_values(self) -> bool:
        """Whether any of the values are missing"""
        return np.any(np.isinf(np.array(self.to_list()).flatten()))

    def to_list(self) -> [[float]]:
        """Converts properties to list

        :return: List of properties in lists
        """
        return [self.__getattribute__(name) for name in Properties.NAMES]

    def from_list(self, params: [object]) -> None:
        """Populate properties using a list of objects

        :param params: List of objects to load it from
        """
        assert len(Properties.NAMES) == len(params)

        # Use custom method to read np array and assign it
        self.d1: np.array = read_np_array(params[0])
        self.d2: np.array = read_np_array(params[1])
        self.d3: np.array = read_np_array(params[2])
        self.d4: np.array = read_np_array(params[3])
        self.a3: np.array = read_np_array(params[4])

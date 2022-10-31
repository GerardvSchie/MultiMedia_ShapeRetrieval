import math
import numpy as np

from src.database.util import read_np_array


class Properties:
    NAMES = [
        "d1", "d2", "d3", "d4", "a3"
    ]

    NR_BINS = 20

    MAX = {
        "d1": np.sqrt(3) / 2,
        "d2": np.sqrt(3),
        "d3": 1,
        "d4": np.cbrt(1 / 3),
        "a3": 1,
    }

    def __init__(self) -> None:
        self.d1: np.array = np.full(Properties.NR_BINS, math.inf)
        self.d2: np.array = np.full(Properties.NR_BINS, math.inf)
        self.d3: np.array = np.full(Properties.NR_BINS, math.inf)
        self.d4: np.array = np.full(Properties.NR_BINS, math.inf)
        self.a3: np.array = np.full(Properties.NR_BINS, math.inf)

    def missing_values(self):
        return np.any(np.isinf(np.array(self.to_list()).flatten()))

    def to_list(self):
        return [self.__getattribute__(name) for name in Properties.NAMES]

    def from_list(self, params: [object]):
        assert len(Properties.NAMES) == len(params)

        self.d1: float = read_np_array(params[0])
        self.d2: float = read_np_array(params[1])
        self.d3: float = read_np_array(params[2])
        self.d4: float = read_np_array(params[3])
        self.a3: float = read_np_array(params[4])

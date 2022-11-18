import numpy as np


class MeshFeatures:
    NAMES = ['nr_vertices', 'nr_faces', 'surface_area', 'volume']

    def __init__(self) -> None:
        """Initializes with dummy values"""
        self.nr_vertices: int = 0
        self.nr_faces: int = 0
        self.surface_area: float = np.inf
        self.volume: float = np.inf

    def misses_values(self) -> bool:
        """Whether there are any mesh features are missing

        :return: Whether any value is missing
        """
        misses_ints = not all([self.nr_vertices, self.nr_faces])
        misses_floats = any([np.isinf(self.surface_area), np.isinf(self.volume)])
        return misses_ints or misses_floats

    def to_list(self):
        """Converts the features to a list

        :return: List with values
        """
        return [self.__getattribute__(name) for name in MeshFeatures.NAMES]

    def from_list(self, params: [object]) -> None:
        """Fill the attributes using the list of values

        :param params: List containing all the parameters
        """
        assert len(MeshFeatures.NAMES) == len(params)

        self.nr_vertices = int(params[0])
        self.nr_faces = int(params[1])
        self.surface_area = float(params[2])
        self.volume = float(params[3])

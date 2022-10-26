import math


class MeshFeatures:
    NAMES = ['nr_vertices', 'nr_faces', 'surface_area', 'volume']

    def __init__(self) -> None:
        self.nr_vertices: int = 0
        self.nr_faces: int = 0
        self.surface_area: float = math.inf
        self.volume: float = math.inf

    def misses_values(self) -> bool:
        misses_ints = not all([self.nr_vertices, self.nr_faces])
        misses_floats = any([math.isinf(self.surface_area), math.isinf(self.volume)])
        return misses_ints or misses_floats

    def to_list(self):
        return [self.__getattribute__(name) for name in MeshFeatures.NAMES]

    def from_list(self, params: [object]):
        assert len(MeshFeatures.NAMES) == len(params)

        self.nr_vertices = int(params[0])
        self.nr_faces = int(params[1])
        self.surface_area = float(params[2])
        self.volume = float(params[3])

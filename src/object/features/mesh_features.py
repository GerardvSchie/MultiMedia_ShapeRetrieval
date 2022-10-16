import math


class MeshFeatures:
    def __init__(self) -> None:
        self.nr_vertices: int = 0
        self.nr_faces: int = 0
        self.surface_area: float = math.inf
        self.volume: float = math.inf
        self.volume_to_surface_ratio: float = math.inf
        self.compactness: float = math.inf
        self.sphericity: float = math.inf
        self.eccentricity: float = math.inf
        self.diameter: float = math.inf
        self.is_watertight: bool = None

    def misses_values(self) -> bool:
        misses_ints = not all([self.nr_vertices, self.nr_faces])
        misses_floats = any([math.isinf(self.surface_area), math.isinf(self.volume),
                             math.isinf(self.volume_to_surface_ratio), math.isinf(self.compactness),
                             math.isinf(self.sphericity), math.isinf(self.eccentricity), math.isinf(self.diameter)])
        misses_bools = self.is_watertight is None

        return misses_ints or misses_floats or misses_bools

import math


class SilhouetteFeatures:
    def __init__(self) -> None:
        self.area: float = math.inf
        self.perimeter: float = math.inf
        self.compactness: float = math.inf
        self.axis_aligned_bounding_box: float = math.inf
        self.rectangularity: float = math.inf
        self.diameter: float = math.inf
        self.eccentricity: float = math.inf

    def misses_values(self):
        return any([math.isinf(self.area), math.isinf(self.perimeter), math.isinf(self.compactness),
                    math.isinf(self.axis_aligned_bounding_box), math.isinf(self.rectangularity),
                    math.isinf(self.diameter), math.isinf(self.eccentricity)
                    ])

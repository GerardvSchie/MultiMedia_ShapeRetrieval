import math
import numpy as np


class SilhouetteFeatures:
    def __init__(self) -> None:
        self.centroid: (float, float) = (math.inf, math.inf)
        self.area: float = math.inf
        self.perimeter: float = math.inf
        self.compactness: float = math.inf
        self.axis_aligned_bounding_box: np.ndarray = np.full((1, 4), math.inf)
        self.rectangularity: float = math.inf
        self.diameter: float = math.inf
        self.eccentricity: float = math.inf

    def misses_values(self):
        return any([math.isinf(self.area), math.isinf(self.perimeter), math.isinf(self.compactness),
                    math.isinf(self.rectangularity),
                    math.isinf(self.diameter), math.isinf(self.eccentricity)
                    ])
        # math.isinf(self.axis_aligned_bounding_box)),
        # Centroid

    def __str__(self):
        return f'c:{self.centroid}, A:{self.area}, P:{self.perimeter}, comp:{self.compactness}, ' \
               f'AABB:{self.axis_aligned_bounding_box}, rec:{self.rectangularity}, diam:{self.diameter}, ' \
               f'ecc:{self.eccentricity}'

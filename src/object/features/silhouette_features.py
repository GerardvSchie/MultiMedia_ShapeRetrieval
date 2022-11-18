import math
import numpy as np


class SilhouetteFeatures:
    def __init__(self) -> None:
        """Initiates all the features with infinite values"""
        self.centroid: (float, float) = (math.inf, math.inf)
        self.area: float = math.inf
        self.perimeter: float = math.inf
        self.compactness: float = math.inf
        self.axis_aligned_bounding_box: np.ndarray = np.full((1, 4), math.inf)
        self.rectangularity: float = math.inf
        self.diameter: float = math.inf
        self.eccentricity: float = math.inf

    def misses_values(self) -> bool:
        """Whether the silhouette feature are missing values

        :return: Whether any value is missing from the silhouette features
        """
        return any([math.isinf(self.area), math.isinf(self.perimeter), math.isinf(self.compactness),
                    math.isinf(self.rectangularity),
                    math.isinf(self.diameter), math.isinf(self.eccentricity)
                    ])

    def __str__(self) -> str:
        """A readable format of the silhouete features

        :return: String representation of the object
        """
        return f'c:{self.centroid}, A:{self.area}, P:{self.perimeter}, comp:{self.compactness}, ' \
               f'AABB:{self.axis_aligned_bounding_box}, rec:{self.rectangularity}, diam:{self.diameter}, ' \
               f'ecc:{self.eccentricity}'

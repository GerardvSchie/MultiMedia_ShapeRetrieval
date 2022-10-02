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

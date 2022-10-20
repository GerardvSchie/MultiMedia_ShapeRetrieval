import math


class Descriptors:
    def __init__(self) -> None:
        self.surface_area: float = math.inf
        self.compactness: float = math.inf
        self.rectangularity: float = math.inf
        self.diameter: float = math.inf
        self.eccentricity: float = math.inf

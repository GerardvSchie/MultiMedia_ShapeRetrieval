import math


class NormalizationFeatures:
    def __init__(self) -> None:
        self.distance_to_center: float = math.inf
        self.scale: float = math.inf
        self.alignment: float = math.inf
        self.rotation: float = math.inf
        self.flip = None

        self.triangle_sizes = []

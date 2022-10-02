import math


class NormalizationFeatures:
    def __init__(self) -> None:
        self.distance_to_center: float = math.inf
        self.scale: float = math.inf
        self.alignment: float = math.inf
        self.flip: float = math.inf

    def misses_values(self) -> bool:
        # TODO: Add flip
        misses_floats = any([math.isinf(self.distance_to_center), math.isinf(self.scale), math.isinf(self.alignment)])
        return misses_floats

import math


class NormalizationFeatures:
    def __init__(self) -> None:
        self.distance_to_center: float = math.inf
        self.scale: float = math.inf
        self.alignment: float = math.inf
        self.flip: int = None

        # Eigenvalues
        self.eigenvalue_s1: float = math.inf
        self.eigenvalue_s2: float = math.inf
        self.eigenvalue_s3: float = math.inf

    def misses_values(self) -> bool:
        misses_ints = self.flip is None
        misses_floats = any([math.isinf(self.distance_to_center), math.isinf(self.scale),
                             math.isinf(self.alignment),
                             math.isinf(self.eigenvalue_s1), math.isinf(self.eigenvalue_s2),
                             math.isinf(self.eigenvalue_s3),
                             ])
        return misses_floats or misses_ints

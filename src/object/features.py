import math


class Features:
    def __init__(self) -> None:
        self.true_class: str = ""

        # General properties
        self.nr_vertices: int = 0
        self.nr_faces: int = 0
        self.type_faces: str = ""

        # Area
        self.mesh_area: float = math.inf
        self.convex_hull_area: float = math.inf
        self.bounding_box_area: float = math.inf

        # Volume
        self.mesh_volume: float = math.inf
        self.convex_hull_volume: float = math.inf
        self.bounding_box_volume: float = math.inf

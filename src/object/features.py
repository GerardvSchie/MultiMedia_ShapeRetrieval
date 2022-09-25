class Features:
    def __init__(self) -> None:
        self.true_class: str = ""

        # General properties
        self.nr_vertices: int = 0
        self.nr_faces: int = 0
        self.type_faces: str = ""

        # Area
        self.mesh_area: float = 0
        self.convex_hull_area: float = 0
        self.bounding_box_area: float = 0

        # Volume
        self.mesh_volume: float = 0
        self.convex_hull_volume: float = 0
        self.bounding_box_volume: float = 0

from src.object.features.mesh_features import MeshFeatures
from src.object.features.silhouette_features import SilhouetteFeatures
from src.object.features.normalization_features import NormalizationFeatures
from src.object.features.bounding_box_features import BoundingBoxFeatures
import math


class ShapeFeatures:
    def __init__(self) -> None:
        self.true_class: str = ""
        self.diameter: float = math.inf
        self.is_watertight: bool = None

        # Features for mesh objects
        self.mesh_features = MeshFeatures()
        self.convex_hull_features = MeshFeatures()
        self.axis_aligned_bounding_box_features = BoundingBoxFeatures()
        self.normalization_features = NormalizationFeatures()

        # 2D features
        self.silhouette_features = SilhouetteFeatures()

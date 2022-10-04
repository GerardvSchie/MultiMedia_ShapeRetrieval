import math

import numpy as np
from src.object.features.mesh_features import MeshFeatures
from src.object.features.silhouette_features import SilhouetteFeatures
from src.object.features.normalization_features import NormalizationFeatures


class ShapeFeatures:
    def __init__(self) -> None:
        self.true_class: str = ""

        # Axis aligned bounding box
        self.aabb_min_bound: np.array = np.array((math.inf, math.inf, math.inf))
        self.aabb_max_bound: np.array = np.array((math.inf, math.inf, math.inf))

        # Features for mesh objects
        self.mesh_features = MeshFeatures()
        self.convex_hull_features = MeshFeatures()
        # self.bounding_box_features = MeshFeatures()

        # Normalization Features
        self.normalization_features = NormalizationFeatures()

        # 2D features
        self.silhouette_features = SilhouetteFeatures()

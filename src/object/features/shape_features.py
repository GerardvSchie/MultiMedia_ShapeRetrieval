import math

from src.object.features.mesh_features import MeshFeatures
from src.object.features.silhouette_features import SilhouetteFeatures
from src.object.features.normalization_features import NormalizationFeatures
from src.object.features.bounding_box_features import BoundingBoxFeatures


class ShapeFeatures:
    NAMES = ['true_class', 'mesh_is_watertight', 'diameter',
        'mesh_nr_vertices', 'mesh_nr_faces', 'mesh_surface_area', 'mesh_volume',
        'convex_hull_nr_vertices', 'convex_hull_nr_faces', 'convex_hull_surface_area', 'convex_hull_volume',
        'bounding_box_p0', 'bounding_box_p1', 'bounding_box_surface_area', 'bounding_box_volume', 'bounding_box_diameter',
        'distance_to_center', 'scale', 'alignment', 'correctly_oriented_axes', 'eigenvalues'
    ]

    def __init__(self) -> None:
        """Initiates all the shape features with dummy variables"""
        self.true_class: str = ""
        self.mesh_is_watertight: bool = None
        self.diameter: float = math.inf

        # Features for mesh objects
        self.mesh_features = MeshFeatures()
        self.convex_hull_features = MeshFeatures()
        self.axis_aligned_bounding_box_features = BoundingBoxFeatures()
        self.normalization_features = NormalizationFeatures()

        # 2D features
        self.silhouette_features = SilhouetteFeatures()

    def to_list(self) -> [object]:
        """Convert all attributes to list format

        :return: List representation of the shape features
        """
        return [self.__getattribute__(name) for name in ShapeFeatures.NAMES[:3]] +\
            self.mesh_features.to_list() + self.convex_hull_features.to_list() +\
            self.axis_aligned_bounding_box_features.to_list() + self.normalization_features.to_list()

    def from_list(self, params: [object]) -> None:
        """Parses the parameters from a list

        :param params: Fill shape features using the
        """
        assert len(ShapeFeatures.NAMES) == len(params)

        self.true_class = params[0]
        self.mesh_is_watertight = params[1].lower() == 'true'
        self.diameter = float(params[2])

        self.mesh_features.from_list(params[3:7])
        self.convex_hull_features.from_list(params[7:11])
        self.axis_aligned_bounding_box_features.from_list(params[11:16])
        self.normalization_features.from_list(params[16:21])

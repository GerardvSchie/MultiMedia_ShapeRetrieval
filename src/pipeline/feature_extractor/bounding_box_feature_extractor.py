import numpy as np
import open3d as o3d
import logging

from src.object.geometries import Geometries
from src.controller.geometries_controller import GeometriesController
from src.object.features.bounding_box_features import BoundingBoxFeatures


class BoundingBoxFeatureExtractor:
    @staticmethod
    # Only extract the features that are not yet set with values in the shape
    def extract_features(mesh: o3d.geometry.TriangleMesh, point_cloud: o3d.geometry.PointCloud, bounding_box: o3d.geometry.AxisAlignedBoundingBox, bounding_box_features: BoundingBoxFeatures, force_recompute=False) -> bool:
        """Extract bounding box features from the bounding box object

        :param mesh: Mesh object
        :param point_cloud: Point cloud object
        :param bounding_box: Bounding box object
        :param bounding_box_features: Features object to save the features to
        :param force_recompute: Force recomputing these features
        :return: Indicates if any feature is recomputed
        """
        if not mesh and not point_cloud and not bounding_box:
            logging.warning("Cannot extract bounding box features without mesh, point cloud, and bounding box")
            return False

        computed_features = [
            BoundingBoxFeatureExtractor.extract_axis_aligned_bounding_box(mesh, point_cloud, bounding_box, bounding_box_features, force_recompute),
            BoundingBoxFeatureExtractor.extract_surface_area(mesh, point_cloud, bounding_box, bounding_box_features, force_recompute),
            BoundingBoxFeatureExtractor.extract_volume(mesh, point_cloud, bounding_box, bounding_box_features, force_recompute),
            BoundingBoxFeatureExtractor.extract_diameter(mesh, point_cloud, bounding_box, bounding_box_features, force_recompute),
        ]

        return any(computed_features)

    @staticmethod
    def extract_axis_aligned_bounding_box(mesh: o3d.geometry.TriangleMesh, point_cloud: o3d.geometry.PointCloud, bounding_box: o3d.geometry.AxisAlignedBoundingBox, bounding_box_features: BoundingBoxFeatures, force_recompute=False) -> bool:
        """Extract two diagonal points of the bounding box

        :param mesh: Mesh object
        :param point_cloud: Point cloud object
        :param bounding_box: Bounding box object
        :param bounding_box_features: Features object to store the features in
        :param force_recompute: Force recomputing the two points
        :return: Indicates if the value is recomputed
        """
        if not any(np.isinf(bounding_box_features.min_bound)) and not any(np.isinf(bounding_box_features.max_bound)) and not force_recompute:
            return False

        bounding_box = BoundingBoxFeatureExtractor._calculate_bounding_box(mesh, point_cloud, bounding_box)

        # Save min and max bound
        bounding_box_features.min_bound = bounding_box.min_bound
        bounding_box_features.max_bound = bounding_box.max_bound
        return True

    @staticmethod
    def extract_surface_area(mesh: o3d.geometry.TriangleMesh, point_cloud: o3d.geometry.PointCloud, bounding_box: o3d.geometry.AxisAlignedBoundingBox, bounding_box_features: BoundingBoxFeatures, force_recompute=False) -> bool:
        """Compute the total surface area of the bounding box

        :param mesh: Mesh object
        :param point_cloud: Point cloud object
        :param bounding_box: Bounding box object
        :param bounding_box_features: Features object to store the features in
        :param force_recompute: Force recomputing the surface area
        :return: Indicates if the value is recomputed
        """
        # Does not need to be recomputed
        if not np.isinf(bounding_box_features.surface_area) and not force_recompute:
            return False

        BoundingBoxFeatureExtractor.extract_axis_aligned_bounding_box(mesh, point_cloud, bounding_box, bounding_box_features, force_recompute)

        # Axes of the shape, multiply them to compute the surface area
        x = abs(bounding_box_features.max_bound[0] - bounding_box_features.min_bound[0])
        y = abs(bounding_box_features.max_bound[1] - bounding_box_features.min_bound[1])
        z = abs(bounding_box_features.max_bound[2] - bounding_box_features.min_bound[2])
        bounding_box_features.surface_area = 2 * x * y + 2 * x * z + 2 * y * z
        return True

    @staticmethod
    def extract_volume(mesh: o3d.geometry.TriangleMesh, point_cloud: o3d.geometry.PointCloud, bounding_box: o3d.geometry.AxisAlignedBoundingBox, bounding_box_features: BoundingBoxFeatures, force_recompute=False) -> bool:
        """Compute the total volume of the bounding box

        :param mesh: Mesh object
        :param point_cloud: Point cloud object
        :param bounding_box: Bounding box object
        :param bounding_box_features: Features object to store the features in
        :param force_recompute: Force recomputing the volume
        :return: Indicates if the value is recomputed
        """
        if not np.isinf(bounding_box_features.volume) and not force_recompute:
            return False

        # Load bounding box and
        bounding_box = BoundingBoxFeatureExtractor._calculate_bounding_box(mesh, point_cloud, bounding_box, force_recompute)
        volume = bounding_box.volume()
        bounding_box_features.volume = volume
        return True

    @staticmethod
    def extract_diameter(mesh: o3d.geometry.TriangleMesh, point_cloud: o3d.geometry.PointCloud,
                         bounding_box: o3d.geometry.AxisAlignedBoundingBox,
                         bounding_box_features: BoundingBoxFeatures, force_recompute=False) -> bool:
        """Compute the total diameter of the bounding box

        :param mesh: Mesh object
        :param point_cloud: Point cloud object
        :param bounding_box: Bounding box object
        :param bounding_box_features: Features object to store the features in
        :param force_recompute: Force recomputing the diameter
        :return: Indicates if the value is recomputed
        """
        if not np.isinf(bounding_box_features.diameter) and not force_recompute:
            return False

        BoundingBoxFeatureExtractor.extract_axis_aligned_bounding_box(mesh, point_cloud, bounding_box,
                                                                                     bounding_box_features,
                                                                                     force_recompute)

        # Axes of the shape
        x2 = np.power(bounding_box_features.max_bound[0] - bounding_box_features.min_bound[0], 2)
        y2 = np.power(bounding_box_features.max_bound[1] - bounding_box_features.min_bound[1], 2)
        z2 = np.power(bounding_box_features.max_bound[2] - bounding_box_features.min_bound[2], 2)

        # Store diameter and indicate the
        bounding_box_features.diameter = np.sqrt(x2 + y2 + z2)
        return True

    @staticmethod
    def _calculate_bounding_box(mesh: o3d.geometry.TriangleMesh, point_cloud: o3d.geometry.PointCloud, bounding_box: o3d.geometry.AxisAlignedBoundingBox, force_recompute=False) -> o3d.geometry.AxisAlignedBoundingBox:
        """Compute the total diameter of the bounding box

        :param mesh: Mesh object
        :param point_cloud: Point cloud object
        :param bounding_box: Bounding box object
        :param force_recompute: Force recomputing the bounding box from the mesh or point cloud
        :return: The axis aligned bounding box
        """
        if bounding_box and not force_recompute:
            return bounding_box

        geometries = Geometries(None)
        geometries.mesh = mesh
        geometries.point_cloud = point_cloud
        GeometriesController.calculate_aligned_bounding_box(geometries)
        return geometries.axis_aligned_bounding_box

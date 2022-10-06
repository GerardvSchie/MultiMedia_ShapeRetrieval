import math
import numpy as np
import open3d as o3d
import logging

from src.object.geometries import Geometries
from src.controller.geometries_controller import GeometriesController
from src.object.features.bounding_box_features import BoundingBoxFeatures


class BoundingBoxFeatureExtractor:
    @staticmethod
    # Only extract the features that are not yet set with values in the shape
    def extract_features(mesh: o3d.geometry.TriangleMesh, point_cloud: o3d.geometry.PointCloud, bounding_box: o3d.geometry.AxisAlignedBoundingBox, bounding_box_features: BoundingBoxFeatures, force_recompute=False):
        if not mesh and not point_cloud and not bounding_box:
            logging.warning("Cannot extract bounding box features without mesh, point cloud, and bounding box")
            return

        BoundingBoxFeatureExtractor.extract_axis_aligned_bounding_box(mesh, point_cloud, bounding_box, bounding_box_features, force_recompute)
        BoundingBoxFeatureExtractor.extract_surface_area(mesh, point_cloud, bounding_box, bounding_box_features, force_recompute)
        BoundingBoxFeatureExtractor.extract_volume(mesh, point_cloud, bounding_box, bounding_box_features, force_recompute)
        BoundingBoxFeatureExtractor.extract_diameter(mesh, point_cloud, bounding_box, bounding_box_features, force_recompute)

    @staticmethod
    def extract_axis_aligned_bounding_box(mesh: o3d.geometry.TriangleMesh, point_cloud: o3d.geometry.PointCloud, bounding_box: o3d.geometry.AxisAlignedBoundingBox, bounding_box_features: BoundingBoxFeatures, force_recompute=False):
        if not any(np.isinf(bounding_box_features.min_bound)) and not any(np.isinf(bounding_box_features.max_bound)) and not force_recompute:
            return

        bounding_box = BoundingBoxFeatureExtractor._calculate_bounding_box(mesh, point_cloud, bounding_box)

        bounding_box_features.min_bound = bounding_box.min_bound
        bounding_box_features.max_bound = bounding_box.max_bound

    @staticmethod
    def extract_surface_area(mesh: o3d.geometry.TriangleMesh, point_cloud: o3d.geometry.PointCloud, bounding_box: o3d.geometry.AxisAlignedBoundingBox, bounding_box_features: BoundingBoxFeatures, force_recompute=False):
        if not math.isinf(bounding_box_features.surface_area) and not force_recompute:
            return

        BoundingBoxFeatureExtractor.extract_axis_aligned_bounding_box(mesh, point_cloud, bounding_box, bounding_box_features, force_recompute)

        # Axes of the shape
        x = abs(bounding_box_features.max_bound[0] - bounding_box_features.min_bound[0])
        y = abs(bounding_box_features.max_bound[1] - bounding_box_features.min_bound[1])
        z = abs(bounding_box_features.max_bound[2] - bounding_box_features.min_bound[2])
        area = 2 * x * y + 2 * x * z + 2 * y * z
        bounding_box_features.surface_area = area

    @staticmethod
    def extract_volume(mesh: o3d.geometry.TriangleMesh, point_cloud: o3d.geometry.PointCloud,
                             bounding_box: o3d.geometry.AxisAlignedBoundingBox,
                             bounding_box_features: BoundingBoxFeatures, force_recompute=False):
        if not math.isinf(bounding_box_features.volume) and not force_recompute:
            return

        bounding_box = BoundingBoxFeatureExtractor._calculate_bounding_box(mesh, point_cloud, bounding_box, force_recompute)
        volume = bounding_box.volume()
        bounding_box_features.volume = volume

    @staticmethod
    def extract_diameter(mesh: o3d.geometry.TriangleMesh, point_cloud: o3d.geometry.PointCloud,
                             bounding_box: o3d.geometry.AxisAlignedBoundingBox,
                             bounding_box_features: BoundingBoxFeatures, force_recompute=False):
        if not math.isinf(bounding_box_features.diameter) and not force_recompute:
            return

        BoundingBoxFeatureExtractor.extract_axis_aligned_bounding_box(mesh, point_cloud, bounding_box,
                                                                                     bounding_box_features,
                                                                                     force_recompute)

        # Axes of the shape
        x2 = np.power(bounding_box_features.max_bound[0] - bounding_box_features.min_bound[0], 2)
        y2 = np.power(bounding_box_features.max_bound[1] - bounding_box_features.min_bound[1], 2)
        z2 = np.power(bounding_box_features.max_bound[2] - bounding_box_features.min_bound[2], 2)

        diameter = np.sqrt(x2 + y2 + z2)
        bounding_box_features.diameter = diameter

    @staticmethod
    def _calculate_bounding_box(mesh: o3d.geometry.TriangleMesh, point_cloud: o3d.geometry.PointCloud, bounding_box: o3d.geometry.AxisAlignedBoundingBox, force_recompute=False):
        if bounding_box and not force_recompute:
            return bounding_box

        geometries = Geometries(None)
        geometries.mesh = mesh
        geometries.point_cloud = point_cloud
        GeometriesController.calculate_aligned_bounding_box(geometries)
        return geometries.axis_aligned_bounding_box

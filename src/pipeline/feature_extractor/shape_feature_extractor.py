import logging

import numpy as np
import math

from src.database.writer import path_to_array
from src.object.shape import Shape
from src.controller.geometries_controller import GeometriesController
from src.pipeline.feature_extractor.bounding_box_feature_extractor import BoundingBoxFeatureExtractor
from src.pipeline.feature_extractor.mesh_feature_extractor import MeshFeatureExtractor
from src.pipeline.feature_extractor.normalization_feature_extractor import NormalizationFeatureExtractor


class ShapeFeatureExtractor:
    @staticmethod
    # Only extract the features that are not yet set with values in the shape
    def extract_all_shape_features(shape: Shape, force_recompute=False) -> bool:
        """Extract all shape features from the given shape

        :param shape: Shape to compute features of
        :param force_recompute: Forces to recompute the features
        :return: Whether features have been recomputed
        """
        if not shape:
            logging.warning("Cannot extract features from None shape")
            return False

        # For each step, remember whether new features are computed
        computed_features = [
            ShapeFeatureExtractor.extract_class_feature(shape, force_recompute),
            ShapeFeatureExtractor.is_watertight(shape, force_recompute),
            ShapeFeatureExtractor.calculate_diameter(shape, force_recompute),
            ShapeFeatureExtractor.extract_mesh_features(shape, force_recompute),
            ShapeFeatureExtractor.extract_convex_hull_features(shape, force_recompute),
            ShapeFeatureExtractor.extract_axis_aligned_bounding_box(shape, force_recompute),
            ShapeFeatureExtractor.extract_normalization_features(shape, force_recompute)
        ]

        return any(computed_features)

    @staticmethod
    def is_watertight(shape: Shape, force_recompute=False) -> bool:
        """Check if shape is watertight and add it as feature

        :param shape: Shape to compute of whether it is watertight
        :param force_recompute: Force recomputing the feature
        :return: Whether it got recomputed
        """
        if shape.features.mesh_is_watertight is not None and not force_recompute:
            return False

        if not shape.geometries.mesh:
            GeometriesController.calculate_mesh(shape.geometries)

        shape.features.mesh_is_watertight = shape.geometries.mesh.is_watertight()
        return True

    @staticmethod
    def calculate_diameter(shape: Shape, force_recompute=False) -> bool:
        """Compute the diameter of the shape, use convex hull to speed up calculations

        :param shape: Shape to compute the diameter of
        :param force_recompute: Force recomputing the feature
        :return: Whether it got recomputed
        """
        if not math.isinf(shape.features.diameter) and not force_recompute:
            return False

        # Compute the convex hull
        GeometriesController.calculate_point_cloud(shape.geometries)
        if not shape.geometries.convex_hull_mesh:
            GeometriesController.calculate_convex_hull(shape.geometries)

        if not shape.geometries.convex_hull_mesh:
            logging.warning('Cannot not compute convex hull without mesh')
            return False

        # At least two points must be in the convex hull
        points = shape.geometries.convex_hull_mesh.vertices
        points = np.asarray(points)

        if len(points) < 2:
            logging.warning('Cannot compute diameter with less than 2 points')
            return False

        # Improve speed by using meshgrid on list of points
        meshgrid_indices = np.array(np.meshgrid(range(len(points)), range(len(points)))).T.reshape(-1, 2)
        values = points[meshgrid_indices]
        vecs = values[:, 0, :] - values[:, 1, :]
        distances = np.linalg.norm(vecs, axis=1)
        shape.features.diameter = np.max(distances)

        #
        return True

    @staticmethod
    def extract_class_feature(shape: Shape, force_recompute=False) -> bool:
        """Extract which class the shape belongs to

        :param shape: Shape to extract the class from
        :param force_recompute: Whether it needs to be recomputed even if it is already set
        :return: Whether the features has been recomputed or not
        """
        if shape.features.true_class and not force_recompute:
            return False

        # Works for two different databases
        if shape.geometries.path.__contains__('LabeledDB_new'):
            arr = path_to_array(shape.geometries.path)
            class_index = np.where(arr == 'LabeledDB_new')[0][0] + 1
            shape.features.true_class = arr[class_index]
            return True
        elif shape.geometries.path.__contains__('Princeton_benchmark'):
            arr = path_to_array(shape.geometries.path)
            class_index = np.where(arr == 'Princeton_benchmark')[0][0] + 3
            pieces = arr[class_index].split('_')
            shape.features.true_class = " ".join(pieces[1:]).capitalize()
            return True
        else:
            logging.warning('Could not extract class from')
            return False

    @staticmethod
    def extract_axis_aligned_bounding_box(shape: Shape, force_recompute=False) -> bool:
        """Gets the axis aligned bounding box of a given shape

        :param shape: Shape to get the AABB of using open3D
        :param force_recompute: Forces re-computation of box even if it had already been loaded
        :return: Whether it has been recomputed
        """
        if not shape.features.axis_aligned_bounding_box_features.misses_values() and not force_recompute:
            return False

        # Compute point cloud
        if not shape.geometries.point_cloud:
            GeometriesController.calculate_point_cloud(shape.geometries)
        GeometriesController.calculate_aligned_bounding_box(shape.geometries)

        return BoundingBoxFeatureExtractor.extract_features(shape.geometries.mesh, shape.geometries.point_cloud, shape.geometries.axis_aligned_bounding_box, shape.features.axis_aligned_bounding_box_features, force_recompute)

    @staticmethod
    def extract_mesh_features(shape: Shape, force_recompute=False) -> bool:
        """Extract all mesh features from the given shape

        :param shape: Shape to compute the mesh features of
        :param force_recompute: Whether to recompute values that had already been computed
        :return: True if a feature got computed
        """
        if not shape.features.mesh_features.misses_values() and not force_recompute:
            return False

        GeometriesController.calculate_mesh(shape.geometries)
        return MeshFeatureExtractor.extract_features(shape.geometries.mesh, shape.features.mesh_features, force_recompute)

    @staticmethod
    def extract_convex_hull_features(shape: Shape, force_recompute=False) -> bool:
        """Extracts all convex hull features of the given shape

        :param shape: Shape to extract convex hull features of
        :param force_recompute: Force computing this
        :return: Whether there have been convex hull features recomputed
        """
        if not shape.features.convex_hull_features.misses_values() and not force_recompute:
            return False

        if GeometriesController.calculate_convex_hull(shape.geometries):
            return MeshFeatureExtractor.extract_features(shape.geometries.convex_hull_mesh, shape.features.convex_hull_features, force_recompute)
        else:
            logging.warning("Could not extract convex hull features")
            return False

    @staticmethod
    def extract_normalization_features(shape: Shape, force_recompute=False) -> bool:
        """Extract normalization features like alignment and barycenter

        :param shape: Shape to compute the features of
        :param force_recompute: Forces recomputing the normalization features
        :return: Whether any normalization features have been recomputed
        """
        if not shape.features.normalization_features.misses_values() and not force_recompute:
            return False

        if not shape.geometries.point_cloud:
            GeometriesController.calculate_point_cloud(shape.geometries)

        return NormalizationFeatureExtractor.extract_features(shape.geometries.point_cloud, shape.features.normalization_features, force_recompute)

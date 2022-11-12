import os
import logging

import numpy as np
import math

from database.writer import path_to_array
from src.object.shape import Shape
from src.controller.geometries_controller import GeometriesController
from src.pipeline.feature_extractor.bounding_box_feature_extractor import BoundingBoxFeatureExtractor
from src.pipeline.feature_extractor.mesh_feature_extractor import MeshFeatureExtractor
from src.pipeline.feature_extractor.normalization_feature_extractor import NormalizationFeatureExtractor


class ShapeFeatureExtractor:
    @staticmethod
    # Only extract the features that are not yet set with values in the shape
    def extract_all_shape_features(shape: Shape, force_recompute=False) -> bool:
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
        if shape.features.mesh_is_watertight is not None and not force_recompute:
            return False

        if not shape.geometries.mesh:
            GeometriesController.calculate_mesh(shape.geometries)

        shape.features.mesh_is_watertight = shape.geometries.mesh.is_watertight()
        return True

    @staticmethod
    def calculate_diameter(shape: Shape, force_recompute=False) -> bool:
        if not math.isinf(shape.features.diameter) and not force_recompute:
            return False

        GeometriesController.calculate_point_cloud(shape.geometries)
        if not shape.geometries.convex_hull_mesh:
            GeometriesController.calculate_convex_hull(shape.geometries)

        if not shape.geometries.convex_hull_mesh:
            logging.warning('Cannot not compute convex hull without mesh')
            return False

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
        max_distance = np.max(distances)
        shape.features.diameter = max_distance
        return True

    @staticmethod
    def extract_class_feature(shape: Shape, force_recompute=False) -> bool:
        if shape.features.true_class and not force_recompute:
            return False

        if shape.geometries.path.__contains__('LabeledDB_new'):
            shape.geometries.path.split(os.pathsep)
            arr = path_to_array(shape.geometries.path)
            class_index = np.where(arr == 'LabeledDB_new')[0][0] + 1
            shape.features.true_class = arr[class_index]
            return True
        else:
            logging.warning('Could not extract class from')
            return False

    @staticmethod
    def extract_axis_aligned_bounding_box(shape: Shape, force_recompute=False) -> bool:
        if not shape.features.axis_aligned_bounding_box_features.misses_values() and not force_recompute:
            return False

        if not shape.geometries.point_cloud:
            GeometriesController.calculate_point_cloud(shape.geometries)
        GeometriesController.calculate_aligned_bounding_box(shape.geometries)

        return BoundingBoxFeatureExtractor.extract_features(shape.geometries.mesh, shape.geometries.point_cloud, shape.geometries.axis_aligned_bounding_box, shape.features.axis_aligned_bounding_box_features, force_recompute)

    @staticmethod
    def extract_mesh_features(shape: Shape, force_recompute=False) -> bool:
        if not shape.features.mesh_features.misses_values() and not force_recompute:
            return False

        GeometriesController.calculate_mesh(shape.geometries)
        return MeshFeatureExtractor.extract_features(shape.geometries.mesh, shape.features.mesh_features, force_recompute)

    @staticmethod
    def extract_convex_hull_features(shape: Shape, force_recompute=False) -> bool:
        if not shape.features.convex_hull_features.misses_values() and not force_recompute:
            return False

        if GeometriesController.calculate_convex_hull(shape.geometries):
            return MeshFeatureExtractor.extract_convex_hull_features(shape.geometries.convex_hull_mesh, shape.features.convex_hull_features, force_recompute)
        else:
            logging.warning("Could not extract convex hull features")
            return False

    @staticmethod
    def extract_normalization_features(shape: Shape, force_recompute=False) -> bool:
        if not shape.features.normalization_features.misses_values() and not force_recompute:
            return False

        if not shape.geometries.point_cloud:
            GeometriesController.calculate_point_cloud(shape.geometries)

        return NormalizationFeatureExtractor.extract_features(shape.geometries.point_cloud, shape.features.normalization_features, force_recompute)

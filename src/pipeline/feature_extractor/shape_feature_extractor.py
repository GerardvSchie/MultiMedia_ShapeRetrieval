import os
import logging
import numpy as np

from src.database.writer import path_to_array
from src.object.shape import Shape
from src.controller.geometries_controller import GeometriesController
from src.pipeline.feature_extractor.bounding_box_feature_extractor import BoundingBoxFeatureExtractor
from src.pipeline.feature_extractor.mesh_feature_extractor import MeshFeatureExtractor
from src.pipeline.feature_extractor.normalization_feature_extractor import NormalizationFeatureExtractor


class ShapeFeatureExtractor:
    @staticmethod
    # Only extract the features that are not yet set with values in the shape
    def extract_all_shape_features(shape: Shape, force_recompute=False):
        if not shape:
            logging.warning("Cannot extract features from None shape")
            return

        ShapeFeatureExtractor.extract_class_feature(shape, force_recompute)
        ShapeFeatureExtractor.extract_axis_aligned_bounding_box(shape, force_recompute)

        ShapeFeatureExtractor.extract_mesh_features(shape, force_recompute)
        ShapeFeatureExtractor.extract_convex_hull_features(shape, force_recompute)
        ShapeFeatureExtractor.extract_normalization_features(shape, force_recompute)

    @staticmethod
    def extract_class_feature(shape: Shape, force_recompute=False):
        if shape.features.true_class and not force_recompute:
            return

        if shape.geometries.path.__contains__('LabeledDB_new'):
            shape.geometries.path.split(os.pathsep)
            arr = path_to_array(shape.geometries.path)
            class_index = np.where(arr == 'LabeledDB_new')[0][0] + 1
            shape.features.true_class = arr[class_index]
        else:
            logging.warning('Could not extract class from')

    @staticmethod
    def extract_axis_aligned_bounding_box(shape: Shape, force_recompute=False):
        if not shape.features.axis_aligned_bounding_box_features.misses_values() and not force_recompute:
            return

        if not shape.geometries.mesh and not shape.geometries.point_cloud:
            GeometriesController.calculate_mesh(shape.geometries)
        GeometriesController.calculate_aligned_bounding_box(shape.geometries)

        BoundingBoxFeatureExtractor.extract_features(shape.geometries.mesh, shape.geometries.point_cloud, shape.geometries.axis_aligned_bounding_box, shape.features.axis_aligned_bounding_box_features, force_recompute)

    @staticmethod
    def extract_mesh_features(shape: Shape, force_recompute=False):
        if not shape.features.mesh_features.misses_values() and not force_recompute:
            return

        GeometriesController.calculate_mesh(shape.geometries)
        MeshFeatureExtractor.extract_features(shape.geometries.mesh, shape.geometries.point_cloud, shape.features.mesh_features, force_recompute)

    @staticmethod
    def extract_convex_hull_features(shape: Shape, force_recompute=False):
        if not shape.features.convex_hull_features.misses_values() and not force_recompute:
            return

        if GeometriesController.calculate_convex_hull(shape.geometries):
            MeshFeatureExtractor.extract_features(shape.geometries.convex_hull_mesh, None, shape.features.convex_hull_features, force_recompute)
        else:
            logging.warning("Could not extract convex hull features")

    @staticmethod
    def extract_normalization_features(shape: Shape, force_recompute=False):
        if not shape.features.normalization_features.misses_values() and not force_recompute:
            return

        if not shape.geometries.mesh and not shape.geometries.point_cloud:
            GeometriesController.calculate_mesh(shape.geometries)

        NormalizationFeatureExtractor.extract_features(shape.geometries.mesh, shape.geometries.point_cloud, shape.geometries.axis_aligned_bounding_box, shape.features.normalization_features, force_recompute)

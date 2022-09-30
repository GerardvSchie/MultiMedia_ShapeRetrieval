import logging
import numpy as np
import math

from src.object.shape import Shape
from src.controller.geometries_controller import GeometriesController
from src.pipeline.normalization import Normalizer


class NormalizationFeatureExtractor:
    @staticmethod
    def extract_normalization_features(shape: Shape, force_recompute=False):
        if shape is None:
            logging.warning("Cannot extract normalization features from None")
            return

        shape.normalization_features.distance_to_center = NormalizationFeatureExtractor.distance_to_center(shape, force_recompute)
        shape.normalization_features.scale = NormalizationFeatureExtractor.mesh_scale(shape, force_recompute)
        shape.normalization_features.alignment = NormalizationFeatureExtractor.mesh_alignment(shape, force_recompute)

    @staticmethod
    def distance_to_center(shape: Shape, force_recompute=False) -> float:
        if not math.isinf(shape.normalization_features.distance_to_center) and not force_recompute:
            return shape.normalization_features.distance_to_center

        if shape.geometries.point_cloud:
            center = shape.geometries.point_cloud.get_center()
        elif GeometriesController.calculate_mesh(shape.geometries):
            center = shape.geometries.mesh.get_center()
        else:
            logging.warning("Cannot compute center without mesh or point cloud")
            return math.inf

        return np.sqrt(np.dot(center, center))

    @staticmethod
    def mesh_scale(shape: Shape, force_recompute=False) -> float:
        if not math.isinf(shape.normalization_features.scale) and not force_recompute:
            return shape.normalization_features.scale

        if GeometriesController.calculate_aligned_bounding_box(shape.geometries):
            return shape.geometries.axis_aligned_bounding_box.get_max_extent()
        elif GeometriesController.calculate_mesh(shape.geometries):
            GeometriesController.calculate_aligned_bounding_box(shape.geometries)
            return shape.geometries.axis_aligned_bounding_box.get_max_extent()
        else:
            logging.warning("Cannot compute center without mesh or point cloud")
            return math.inf

    @staticmethod
    def mesh_alignment(shape: Shape, force_recompute=False) -> float:
        if not math.isinf(shape.normalization_features.alignment) and not force_recompute:
            return shape.normalization_features.alignment

        # Computed over the point cloud
        if not shape.geometries.point_cloud:
            GeometriesController.calculate_mesh(shape.geometries)
            GeometriesController.calculate_point_cloud(shape.geometries)

        # Compute the eigenvalues and vectors
        eigenvalues_eigenvectors = Normalizer.get_eigenvalues_and_eigenvectors(shape.geometries.point_cloud)

        # Dot product with each vector component
        col1 = abs(np.dot(eigenvalues_eigenvectors[0][1], np.array([1, 0, 0])))
        col2 = abs(np.dot(eigenvalues_eigenvectors[1][1], np.array([0, 1, 0])))
        col3 = abs(np.dot(eigenvalues_eigenvectors[2][1], np.array([0, 0, 1])))

        # Return the average dot product
        return (col1 + col2 + col3) / 3

import logging
import numpy as np
import math
import open3d as o3d

from src.pipeline.normalization import Normalizer
from src.object.features.normalization_features import NormalizationFeatures


class NormalizationFeatureExtractor:
    @staticmethod
    def extract_features(point_cloud: o3d.geometry.PointCloud, normalization_features: NormalizationFeatures, force_recompute=False):
        if not point_cloud:
            logging.warning("Cannot extract any normalization features without point cloud")
            return

        NormalizationFeatureExtractor.distance_to_center(point_cloud, normalization_features, force_recompute)
        NormalizationFeatureExtractor.mesh_scale(point_cloud, normalization_features, force_recompute)
        NormalizationFeatureExtractor.mesh_alignment(point_cloud, normalization_features, force_recompute)
        NormalizationFeatureExtractor.mesh_eigenvalues(point_cloud, normalization_features, force_recompute)
        NormalizationFeatureExtractor.mesh_flip(point_cloud, normalization_features, force_recompute)

    @staticmethod
    def distance_to_center(point_cloud: o3d.geometry.PointCloud, normalization_features: NormalizationFeatures, force_recompute=False) -> None:
        if not math.isinf(normalization_features.distance_to_center) and not force_recompute:
            return

        if point_cloud:
            center = point_cloud.get_center()
        else:
            logging.warning("Cannot compute center without mesh or point cloud")
            return

        distance = np.sqrt(np.dot(center, center))
        normalization_features.distance_to_center = distance

    @staticmethod
    def mesh_scale(point_cloud: o3d.geometry.PointCloud, normalization_features: NormalizationFeatures, force_recompute=False) -> None:
        if not math.isinf(normalization_features.scale) and not force_recompute:
            return

        if point_cloud:
            scale = point_cloud.get_axis_aligned_bounding_box().get_max_extent()
        else:
            logging.warning("Cannot compute scale without mesh, bounding box or point cloud")
            return

        normalization_features.scale = scale

    @staticmethod
    def mesh_alignment(point_cloud: o3d.geometry.PointCloud, normalization_features: NormalizationFeatures, force_recompute=False) -> None:
        if not math.isinf(normalization_features.alignment) and not force_recompute:
            return

        # Computed over the point cloud
        if point_cloud:
            eigenvalues_eigenvectors = Normalizer.get_eigenvalues_and_eigenvectors(point_cloud)
        else:
            logging.warning("Cannot compute alignment without mesh or point cloud")
            return

        # Dot product with each vector component
        col1 = abs(np.dot(eigenvalues_eigenvectors[0][1], np.array([1, 0, 0])))
        col2 = abs(np.dot(eigenvalues_eigenvectors[1][1], np.array([0, 1, 0])))
        col3 = abs(np.dot(eigenvalues_eigenvectors[2][1], np.array([0, 0, 1])))

        # Return the average dot product
        alignment = (col1 + col2 + col3) / 3
        normalization_features.alignment = alignment

    @staticmethod
    def mesh_flip(point_cloud: o3d.geometry.PointCloud, normalization_features: NormalizationFeatures, force_recompute=False) -> None:
        if normalization_features.flip is not None and not force_recompute:
            return

        # Computed over the point cloud
        if point_cloud:
            fi = Normalizer.compute_fi(point_cloud)
        else:
            logging.warning("Cannot compute alignment without point cloud")
            return

        correctly_flipped_axes = sum(np.clip(fi, 0, 1))
        normalization_features.flip = int(correctly_flipped_axes)

    @staticmethod
    def mesh_eigenvalues(point_cloud: o3d.geometry.PointCloud, normalization_features: NormalizationFeatures, force_recompute=False) -> None:
        if not any(np.isinf(normalization_features.eigenvalues)) and not force_recompute:
            return

        # Computed over the point cloud
        if point_cloud:
            eigenvalues_eigenvectors = Normalizer.get_eigenvalues_and_eigenvectors(point_cloud)
        else:
            logging.warning("Cannot compute alignment without mesh or point cloud")
            return

        normalization_features.eigenvalues = \
            np.array([eigenvalues_eigenvectors[0][0], eigenvalues_eigenvectors[1][0], eigenvalues_eigenvectors[2][0]])

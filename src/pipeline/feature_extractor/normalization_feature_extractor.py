import logging
import numpy as np
import math
import open3d as o3d

from src.pipeline.normalization import Normalizer
from src.object.features.normalization_features import NormalizationFeatures


class NormalizationFeatureExtractor:
    @staticmethod
    def extract_features(point_cloud: o3d.geometry.PointCloud, normalization_features: NormalizationFeatures, force_recompute=False) -> bool:
        """Extract normalize features from the shape

        :param point_cloud: Point cloud of the shape
        :param normalization_features: Feature object to fill with the features
        :param force_recompute: Force the features to be recomputed
        :return: Whether features have been recomputed
        """
        if not point_cloud:
            logging.warning("Cannot extract any normalization features without point cloud")
            return False

        # Contains which features have been recomputed
        computed_features = [
            NormalizationFeatureExtractor.distance_to_center(point_cloud, normalization_features, force_recompute),
            NormalizationFeatureExtractor.mesh_scale(point_cloud, normalization_features, force_recompute),
            NormalizationFeatureExtractor.mesh_alignment(point_cloud, normalization_features, force_recompute),
            NormalizationFeatureExtractor.mesh_eigenvalues(point_cloud, normalization_features, force_recompute),
            NormalizationFeatureExtractor.mesh_flip(point_cloud, normalization_features, force_recompute),
        ]

        # Whether features have been recomputed
        return any(computed_features)

    @staticmethod
    def distance_to_center(point_cloud: o3d.geometry.PointCloud, normalization_features: NormalizationFeatures, force_recompute=False) -> bool:
        """Compute the distance to the bary center

        :param point_cloud: Point cloud to compute the barycenter of
        :param normalization_features: Object the computed barycenter gets saved to
        :param force_recompute: Force recomputing the barycenter
        :return: Whether the feature was recomputed
        """
        if not math.isinf(normalization_features.distance_to_center) and not force_recompute:
            return False

        if point_cloud:
            center = point_cloud.get_center()
        else:
            logging.warning("Cannot compute center without mesh or point cloud")
            return False

        distance = np.sqrt(np.dot(center, center))
        normalization_features.distance_to_center = distance
        return True

    @staticmethod
    def mesh_scale(point_cloud: o3d.geometry.PointCloud, normalization_features: NormalizationFeatures, force_recompute=False) -> bool:
        """Compute the scale of the mesh

        :param point_cloud: Point cloud to compute the scale, or max extend of
        :param normalization_features: Object the computed scale gets saved to
        :param force_recompute: Force recomputing the scale
        :return: Whether the feature was recomputed
        """
        if not math.isinf(normalization_features.scale) and not force_recompute:
            return False

        if point_cloud:
            scale = point_cloud.get_axis_aligned_bounding_box().get_max_extent()
        else:
            logging.warning("Cannot compute scale without mesh, bounding box or point cloud")
            return False

        normalization_features.scale = scale
        return True

    @staticmethod
    def mesh_alignment(point_cloud: o3d.geometry.PointCloud, normalization_features: NormalizationFeatures, force_recompute=False) -> bool:
        """Compute the alignment of a mesh using the point cloud

        :param point_cloud: Point cloud to compute alignment
        :param normalization_features: Object the computed alignment gets saved to
        :param force_recompute: Force recomputing the alignment
        :return: Whether the feature was recomputed
        """
        if not math.isinf(normalization_features.alignment) and not force_recompute:
            return False

        # Computed over the point cloud
        if point_cloud:
            eigenvalues_eigenvectors = Normalizer.get_eigenvalues_and_eigenvectors(point_cloud)
        else:
            logging.warning("Cannot compute alignment without mesh or point cloud")
            return False

        # Dot product with each vector component
        col1 = abs(np.dot(eigenvalues_eigenvectors[0][1], np.array([1, 0, 0])))
        col2 = abs(np.dot(eigenvalues_eigenvectors[1][1], np.array([0, 1, 0])))
        col3 = abs(np.dot(eigenvalues_eigenvectors[2][1], np.array([0, 0, 1])))

        # Return the average dot product
        alignment = (col1 + col2 + col3) / 3
        normalization_features.alignment = alignment
        return True

    @staticmethod
    def mesh_flip(point_cloud: o3d.geometry.PointCloud, normalization_features: NormalizationFeatures, force_recompute=False) -> bool:
        """Return the amount of correctly flipped axis

        :param point_cloud: Point cloud of which the eigenvalues are computed
        :param normalization_features: Object to save the values to
        :param force_recompute: Force recomputing the
        :return: Whether the eigenvalues are recomputed
        """
        if normalization_features.flip is not None and not force_recompute:
            return False

        # Computed over the point cloud
        if point_cloud:
            fi = Normalizer.compute_fi(point_cloud)
        else:
            logging.warning("Cannot compute alignment without point cloud")
            return False

        # Number of correctly aligned axes
        correctly_flipped_axes = sum(np.clip(fi, 0, 1))
        normalization_features.flip = int(correctly_flipped_axes)
        return True

    @staticmethod
    def mesh_eigenvalues(point_cloud: o3d.geometry.PointCloud, normalization_features: NormalizationFeatures, force_recompute=False) -> bool:
        """Compute the eigenvalues of the mesh

        :param point_cloud: Point cloud of which the eigenvalues are computed
        :param normalization_features: Object to save the values to
        :param force_recompute: Force recomputing the
        :return: Whether the eigenvalues are recomputed
        """
        if not any(np.isinf(normalization_features.eigenvalues)) and not force_recompute:
            return False

        # Computed over the point cloud
        if point_cloud:
            eigenvalues_eigenvectors = Normalizer.get_eigenvalues_and_eigenvectors(point_cloud)
        else:
            logging.warning("Cannot compute alignment without mesh or point cloud")
            return False

        # Eigenvalues
        normalization_features.eigenvalues = \
            np.array([eigenvalues_eigenvectors[0][0], eigenvalues_eigenvectors[1][0], eigenvalues_eigenvectors[2][0]])
        return True

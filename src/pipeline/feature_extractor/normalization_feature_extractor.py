import logging
import numpy as np
import math
import open3d as o3d

from src.pipeline.normalization import Normalizer
from src.object.features.normalization_features import NormalizationFeatures


class NormalizationFeatureExtractor:
    @staticmethod
    def extract_features(mesh: o3d.geometry.TriangleMesh, point_cloud: o3d.geometry.PointCloud, bounding_box: o3d.geometry.AxisAlignedBoundingBox, normalization_features: NormalizationFeatures, force_recompute=False):
        if not mesh and not point_cloud:
            logging.warning("Cannot extract any normalization features without mesh and point cloud")
            return

        NormalizationFeatureExtractor.distance_to_center(mesh, point_cloud, normalization_features, force_recompute)
        NormalizationFeatureExtractor.mesh_scale(mesh, point_cloud, bounding_box, normalization_features, force_recompute)
        NormalizationFeatureExtractor.mesh_alignment(mesh, point_cloud, normalization_features, force_recompute)
        NormalizationFeatureExtractor.mesh_eigenvalues(mesh, point_cloud, normalization_features, force_recompute)

        if mesh:
            NormalizationFeatureExtractor.mesh_flip(mesh, normalization_features, force_recompute)
        else:
            logging.warning('Was not able to do flip test without mesh')

    @staticmethod
    def distance_to_center(mesh: o3d.geometry.TriangleMesh, point_cloud: o3d.geometry.PointCloud, normalization_features: NormalizationFeatures, force_recompute=False) -> None:
        if not math.isinf(normalization_features.distance_to_center) and not force_recompute:
            return

        if point_cloud:
            center = point_cloud.get_center()
        elif mesh:
            center = mesh.get_center()
        else:
            logging.warning("Cannot compute center without mesh or point cloud")
            return

        distance = np.sqrt(np.dot(center, center))
        normalization_features.distance_to_center = distance

    @staticmethod
    def mesh_scale(mesh: o3d.geometry.TriangleMesh, point_cloud: o3d.geometry.PointCloud, bounding_box: o3d.geometry.AxisAlignedBoundingBox, normalization_features: NormalizationFeatures, force_recompute=False) -> None:
        if not math.isinf(normalization_features.scale) and not force_recompute:
            return

        if bounding_box:
            scale = bounding_box.get_max_extent()
        elif point_cloud:
            scale = point_cloud.get_axis_aligned_bounding_box().get_max_extent()
        elif mesh:
            scale = mesh.get_axis_aligned_bounding_box().get_max_extent()
        else:
            logging.warning("Cannot compute scale without mesh, bounding box or point cloud")
            return

        normalization_features.scale = scale

    @staticmethod
    def mesh_alignment(mesh: o3d.geometry.TriangleMesh, point_cloud: o3d.geometry.PointCloud, normalization_features: NormalizationFeatures, force_recompute=False) -> None:
        if not math.isinf(normalization_features.alignment) and not force_recompute:
            return

        # Computed over the point cloud
        if point_cloud:
            eigenvalues_eigenvectors = Normalizer.get_eigenvalues_and_eigenvectors(point_cloud)
        elif mesh:
            eigenvalues_eigenvectors = Normalizer.get_eigenvalues_and_eigenvectors(o3d.geometry.PointCloud(mesh.vertices))
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
    def mesh_flip(mesh: o3d.geometry.TriangleMesh, normalization_features: NormalizationFeatures, force_recompute=False) -> None:
        if normalization_features.flip is not None and not force_recompute:
            return

        # Computed over the point cloud
        if mesh:
            fi = Normalizer.compute_fi(mesh)
        else:
            logging.warning("Cannot compute alignment without mesh or point cloud")
            return

        correctly_flipped_axes = sum(np.clip(fi, 0, 1))
        normalization_features.flip = correctly_flipped_axes

    @staticmethod
    def mesh_eigenvalues(mesh: o3d.geometry.TriangleMesh, point_cloud: o3d.geometry.PointCloud, normalization_features: NormalizationFeatures, force_recompute=False) -> None:
        if (not math.isinf(normalization_features.eigenvalue_s1) or not math.isinf(normalization_features.eigenvalue_s2) or not math.isinf(normalization_features.eigenvalue_s3)) and not force_recompute:
            return

        # Computed over the point cloud
        if point_cloud:
            eigenvalues_eigenvectors = Normalizer.get_eigenvalues_and_eigenvectors(point_cloud)
        elif mesh:
            eigenvalues_eigenvectors = Normalizer.get_eigenvalues_and_eigenvectors(o3d.geometry.PointCloud(mesh.vertices))
        else:
            logging.warning("Cannot compute alignment without mesh or point cloud")
            return

        normalization_features.eigenvalue_s1 = eigenvalues_eigenvectors[0][0]
        normalization_features.eigenvalue_s2 = eigenvalues_eigenvectors[1][0]
        normalization_features.eigenvalue_s3 = eigenvalues_eigenvectors[2][0]

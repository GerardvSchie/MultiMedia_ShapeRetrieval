import logging

import open3d as o3d
import numpy as np

from src.controller.geometries_controller import GeometriesController
from src.object.shape import Shape


class Normalizer:
    @staticmethod
    def normalize_shape(shape: Shape):
        if not shape.geometries.point_cloud:
            logging.warning('Failed to normalize shape')
            return False

        # Translate to center
        Normalizer.translater(shape)
        # Rotate based on PCA
        Normalizer.rot_pca(shape)
        # Flip based on momentum
        Normalizer.flipper_vertices_center(shape.geometries.point_cloud)
        # Scale shape to unit size
        Normalizer.scaler(shape)

        return True

    @staticmethod
    def reconstruct_shape(shape: Shape):
        # All other parts need to get recomputed
        GeometriesController.calculate_all_from_mesh(shape.geometries, True)
        GeometriesController.calculate_mesh_normals(shape.geometries, True)
        GeometriesController.calculate_point_cloud_normals(shape.geometries, True)

    @staticmethod
    def translater(shape):
        bary_center = shape.geometries.point_cloud.get_center()
        shape.geometries.point_cloud.translate(-bary_center)

    @staticmethod
    def scaler(shape):
        scale_before = shape.geometries.point_cloud.get_axis_aligned_bounding_box().get_max_extent()
        shape.geometries.point_cloud.scale(1 / scale_before, shape.geometries.point_cloud.get_center())

    @staticmethod
    def rot_pca(shape: Shape):
        sort = Normalizer.get_eigenvalues_and_eigenvectors(shape.geometries.point_cloud)
        rotation_matrix = np.array([sort[0][1], sort[1][1], sort[2][1]])

        # Depending on the determinant of the rotation matrix
        # rotate with positive or negative matrix
        if np.linalg.det(rotation_matrix) >= 0:
            shape.geometries.point_cloud.rotate(R=rotation_matrix)
        else:
            shape.geometries.point_cloud.rotate(R=-rotation_matrix)

        # Verify eigenvalues of new mesh
        Normalizer.get_eigenvalues_and_eigenvectors(shape.geometries.point_cloud)

    @staticmethod
    def get_eigenvalues_and_eigenvectors(pcd: o3d.geometry.PointCloud):
        mean, covariance = pcd.compute_mean_and_covariance()
        eigenvalues, eigenvectors = np.linalg.eig(covariance)

        zipped = [
            (eigenvalues[0], eigenvectors[:, 0]),
            (eigenvalues[1], eigenvectors[:, 1]),
            (eigenvalues[2], eigenvectors[:, 2]),
        ]

        return sorted(zipped, key=lambda x: x[0], reverse=True)

    @staticmethod
    def flipper_vertices_center(pcd: o3d.geometry.PointCloud):
        fi = Normalizer.compute_fi(pcd)
        flipping_rotation_matrix = np.zeros((3, 3))
        np.fill_diagonal(flipping_rotation_matrix, fi)
        pcd.rotate(R=flipping_rotation_matrix)

    @staticmethod
    def compute_fi(pcd: o3d.geometry.PointCloud):
        fi = np.array([0, 0, 0], dtype=float)

        points = np.asarray(pcd.points)
        for point in points:
            fi += np.sign(point) * np.power(point, 2)

        return np.sign(fi)

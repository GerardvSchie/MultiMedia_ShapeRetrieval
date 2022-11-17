import logging

import open3d as o3d
import numpy as np

from src.controller.geometries_controller import GeometriesController
from src.object.shape import Shape


class Normalizer:
    @staticmethod
    def normalize_shape(shape: Shape) -> bool:
        """Normalize the given shape

        :param shape: Shape to normalize
        :return: Whether shape has been normalized
        """
        if not shape.geometries.point_cloud:
            logging.warning('Failed to normalize shape')
            return False

        # Translate to center
        Normalizer.translater(shape)
        # Rotate based on PCA
        Normalizer.rot_pca(shape)
        # Flip based on momentum
        Normalizer.flipper_vertices_center(shape)
        # Scale shape to unit size
        Normalizer.scaler(shape)

        return True

    @staticmethod
    def reconstruct_shape(shape: Shape) -> None:
        """All other parts need to get recomputed

        :param shape: Shape to create the other geometries for
        """
        GeometriesController.calculate_all_from_mesh(shape.geometries, True)
        GeometriesController.calculate_mesh_normals(shape.geometries, True)
        GeometriesController.calculate_point_cloud_normals(shape.geometries, True)

    @staticmethod
    def translater(shape: Shape) -> None:
        """Translate the shape to the barycenter

        :param shape:
        :return:
        """
        bary_center = shape.geometries.point_cloud.get_center()
        shape.geometries.point_cloud.translate(-bary_center)
        shape.geometries.mesh.translate(-bary_center)

    @staticmethod
    def scaler(shape: Shape) -> None:
        """Scale shape to unit cube size (edges of length 1)

        :param shape: Shape to scale to unit cube
        """
        scale_before = shape.geometries.point_cloud.get_axis_aligned_bounding_box().get_max_extent()
        barycenter = shape.geometries.point_cloud.get_center()
        shape.geometries.point_cloud.scale(1 / scale_before, barycenter)
        shape.geometries.mesh.scale(1 / scale_before, barycenter)

    @staticmethod
    def rot_pca(shape: Shape) -> None:
        """Rotate the shape with a rotation matrix using PCA

        :param shape: Shape to rotate
        """
        sort = Normalizer.get_eigenvalues_and_eigenvectors(shape.geometries.point_cloud)
        rotation_matrix = np.array([sort[0][1], sort[1][1], sort[2][1]])

        # Depending on the determinant of the rotation matrix
        # rotate with positive or negative matrix
        if np.linalg.det(rotation_matrix) >= 0:
            shape.geometries.point_cloud.rotate(R=rotation_matrix)
            shape.geometries.mesh.rotate(R=rotation_matrix)
        else:
            shape.geometries.point_cloud.rotate(R=-rotation_matrix)
            shape.geometries.mesh.rotate(R=-rotation_matrix)

    @staticmethod
    def get_eigenvalues_and_eigenvectors(pcd: o3d.geometry.PointCloud) -> [(float, np.array)]:
        """Compute the eigenvalues and eigenvectors and returns them in sorted order

        :param pcd: Point cloud to compute the eigenvalues and eigenvectors of
        :return: Eigenvalue combined with the eigenvector in sorted order
        """
        mean, covariance = pcd.compute_mean_and_covariance()
        eigenvalues, eigenvectors = np.linalg.eig(covariance)

        # Zip so sorting can be performed
        zipped = [
            (eigenvalues[0], eigenvectors[:, 0]),
            (eigenvalues[1], eigenvectors[:, 1]),
            (eigenvalues[2], eigenvectors[:, 2]),
        ]

        # Sorted eigenvectors
        return sorted(zipped, key=lambda x: x[0], reverse=True)

    @staticmethod
    def flipper_vertices_center(shape: Shape) -> None:
        """Flip vertices in x,y,z direction based on their momentum

        :param shape: Shape to flip the axis of
        """
        # Computes rotation matrix based on momentum test
        fi = Normalizer.compute_fi(shape.geometries.point_cloud)
        flipping_rotation_matrix = np.zeros((3, 3))
        np.fill_diagonal(flipping_rotation_matrix, fi)

        # Rotate both the point cloud and the mesh
        shape.geometries.point_cloud.rotate(R=flipping_rotation_matrix)
        shape.geometries.mesh.rotate(R=flipping_rotation_matrix)

        # If determinant is lower than 0 then order of vertices in triangles need to get swapped
        if np.linalg.det(flipping_rotation_matrix) < 0:
            shape.geometries.mesh.triangles = o3d.utility.Vector3iVector(np.flip(np.asarray(shape.geometries.mesh.triangles), axis=1))

    @staticmethod
    def compute_fi(pcd: o3d.geometry.PointCloud) -> np.array:
        """Computes the volume on each side and returns which axis need to get flipped

        :param pcd: Point cloud to compute it on
        :return: Vector with 1 if axis is correctly aligned and -1 if it needs to get flipped
        """
        fi = np.array([0, 0, 0], dtype=float)

        points = np.asarray(pcd.points)
        for point in points:
            fi += np.sign(point) * np.power(point, 2)

        return np.sign(fi)

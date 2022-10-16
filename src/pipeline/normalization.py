import open3d as o3d
import numpy as np

from src.controller.geometries_controller import GeometriesController
from src.object.shape import Shape


class Normalizer:
    @staticmethod
    def normalize_shape(shape: Shape):
        GeometriesController.calculate_mesh(shape.geometries)
        # Translate to center
        shape.geometries.mesh.translate(-shape.geometries.mesh.get_center())
        # Rotate based on PCA
        Normalizer.rot_pca(shape)
        # Flip based on momentum
        Normalizer.flipper_vertices_center(shape.geometries.mesh)
        # Scale shape to unit size
        Normalizer.scaler(shape)

    @staticmethod
    def reconstruct_shape(shape: Shape):
        # All other parts need to get recomputed
        GeometriesController.calculate_all_from_mesh(shape.geometries, True)
        GeometriesController.calculate_mesh_normals(shape.geometries, True)
        GeometriesController.calculate_point_cloud_normals(shape.geometries, True)

    @staticmethod
    def scaler(shape):
        scale_before = shape.geometries.mesh.get_axis_aligned_bounding_box().get_max_extent()
        shape.geometries.mesh.scale(1 / scale_before, shape.geometries.mesh.get_center())
        scale_after = shape.geometries.mesh.get_axis_aligned_bounding_box().get_max_extent()
        print(scale_before, '->', scale_after)

    @staticmethod
    def rot_pca(shape: Shape):
        sort = Normalizer.get_eigenvalues_and_eigenvectors(shape.geometries.point_cloud)
        rotation_matrix = np.array([sort[0][1], sort[1][1], sort[2][1]])

        # Depending on the determinant of the rotation matrix
        # rotate with positive or negative matrix
        if np.linalg.det(rotation_matrix) >= 0:
            shape.geometries.mesh.rotate(R=rotation_matrix)
        else:
            shape.geometries.mesh.rotate(R=-rotation_matrix)

        # Verify eigenvalues of new mesh
        point_cloud = o3d.geometry.PointCloud(shape.geometries.mesh.vertices)
        Normalizer.get_eigenvalues_and_eigenvectors(point_cloud)

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
    def flipper_vertices_center(mesh: o3d.geometry.TriangleMesh):
        fi = Normalizer.compute_fi(mesh)
        flipping_rotation_matrix = np.zeros((3, 3))
        np.fill_diagonal(flipping_rotation_matrix, fi)

        mesh.rotate(R=flipping_rotation_matrix)
        # For a negative determinant the order of the points in the triangles is flipped.
        if np.linalg.det(flipping_rotation_matrix) < 0:
            mesh.triangles = o3d.utility.Vector3iVector(np.flip(np.asarray(mesh.triangles), axis=1))

    @staticmethod
    def compute_fi(mesh: o3d.geometry.TriangleMesh):
        fi = np.array([0, 0, 0], dtype=float)

        vertices = np.asarray(mesh.vertices)
        for point_indices in mesh.triangles:
            # Center of mass == Centroid
            # Definitely scientific source: https://www.quora.com/What-is-the-difference-between-a-centroid-and-a-centre-of-mass
            points = vertices[point_indices]
            # Sum each coordinate and average
            center_of_mass = np.sum(points, axis=0) / 3
            # Add for each axis to fi
            fi += np.sign(center_of_mass) * np.power(center_of_mass, 2)

        return np.sign(fi)

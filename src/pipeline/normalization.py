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

        Normalizer.rot_pca(shape)  # Rotate based on PCA
        # shape.geometries.mesh = flipper(shape.geometries.mesh)  # Flips the mesh
        # shape.geometries.mesh = scaler(shape.geometries.mesh)  # Scales to a unit bounding box the mesh

        # All other parts need to get recomputed
        GeometriesController.calculate_all_from_mesh(shape.geometries, True)
        GeometriesController.calculate_mesh_normals(shape.geometries, True)
        GeometriesController.calculate_point_cloud_normals(shape.geometries, True)

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

        # print(eigenvalues)
        # print(eigenvectors)

        zipped = [
            (eigenvalues[0], eigenvectors[:, 0]),
            (eigenvalues[1], eigenvectors[:, 1]),
            (eigenvalues[2], eigenvectors[:, 2]),
        ]

        return sorted(zipped, key=lambda x: x[0], reverse=True)

    @staticmethod
    def flipper(mesh):
        # verts = mesh.vertices
        return mesh

    @staticmethod
    def scaler(mesh):
        verts = mesh.vertices
        xc = [x[0] for x in verts]
        yc = [x[1] for x in verts]
        zc = [x[2] for x in verts]
        xmin, xmax = min(xc), max(xc)
        ymin, ymax = min(yc), max(yc)
        zmin, zmax = min(zc), max(zc)
        maxbox = max([xmax - xmin, ymax - ymin, zmax - zmin])
        mesh.vertices /= maxbox
        return mesh

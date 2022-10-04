import open3d as o3d
import numpy as np
import logging

from src.controller.geometries_controller import GeometriesController
from src.object.shape import Shape


class Normalizer:
    @staticmethod
    def normalize_shape(shape: Shape):
        GeometriesController.calculate_mesh(shape.geometries)
        # Translate to center
        shape.geometries.mesh.translate(-shape.geometries.mesh.get_center())
        # Scale shape to unit size
        Normalizer.scaler(shape)
        # Rotate based on PCA
        Normalizer.rot_pca(shape)
        # Flip based on momentum
        Normalizer.flipper(shape.geometries.mesh)

        # All other parts need to get recomputed
        GeometriesController.calculate_all_from_mesh(shape.geometries, True)
        GeometriesController.calculate_mesh_normals(shape.geometries, True)
        GeometriesController.calculate_point_cloud_normals(shape.geometries, True)

    @staticmethod
    def scaler(shape):
        scale = shape.geometries.mesh.get_axis_aligned_bounding_box().get_max_extent()
        shape.geometries.mesh.scale(1 / scale, shape.geometries.mesh.get_center())

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
        return
        faces = ( index, ( xcoord, ycoord, zcoord )  )

        triangles = np.zeros((3, len(faces)))
        for i, indexes in enumerate(faces):
            xc, yc, zc = [], [], []
            for inum in indexes:
                verts = mesh.vertices[inum]
                xc.append(verts[0])
                yc.append(verts[1])
                zc.append(verts[2])
            triangles[0][i] = np.sum(xc) / 3
            triangles[1][i] = np.sum(yc) / 3
            triangles[2][i] = np.sum(zc) / 3

            sx = 0
            for x in triangles[0]:
                sx += np.sign(x) * (x ** 2)

            sy = 0
            for y in triangles[1]:
                sy += np.sign(y) * (y ** 2)

            sz = 0
            for z in triangles[2]:
                sz += np.sign(z) * (z ** 2)

            flipping = np.array([[np.sign(sx), 0, 0], [0, np.sign(sy), 0], [0, 0, np.sign(sz)]])

            mesh.vertices = np.matmul(mesh.vertices, flipping)

        return mesh

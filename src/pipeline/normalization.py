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
        # Scale shape to unit size
        Normalizer.scaler(shape)
        # Rotate based on PCA
        Normalizer.rot_pca(shape)
        # Flip based on momentum
        Normalizer.flipper_vertices_center(shape.geometries.mesh)

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
        print('---------')
        print(rotation_matrix)
        print(np.linalg.det(rotation_matrix))
        if np.linalg.det(rotation_matrix) >= 0:
            print('positive rotation matrix')
            shape.geometries.mesh.rotate(R=rotation_matrix)
        else:
            print('negative rotation matrix')
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
        np.fill_diagonal(flipping_rotation_matrix, np.sign(fi))
        mesh.rotate(flipping_rotation_matrix)

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

        return fi

    @staticmethod
    def flipper_vertices(mesh: o3d.geometry.TriangleMesh):
        fx = 0
        fy = 0
        fz = 0

        for point in mesh.vertices:
            fx += np.sign(point[0]) * np.power(point[0], 2)
            fy += np.sign(point[1]) * np.power(point[1], 2)
            fz += np.sign(point[2]) * np.power(point[2], 2)

        print(fx, fy, fz)

        # Flipping is done at the end of the calculation
        if np.sign(fx) == -1:
            print('point: flipped along X')
        if np.sign(fy) == -1:
            print('point: flipped along Y')
        if np.sign(fz) == -1:
            print('point: flipped along Z')

        flipping_matrix = np.array([[np.sign(fx), 0, 0], [0, np.sign(fy), 0], [0, 0, np.sign(fz)]])
        mesh.rotate(flipping_matrix)

    @staticmethod
    def flipper(mesh: o3d.geometry.TriangleMesh):
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

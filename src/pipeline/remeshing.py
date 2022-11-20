import open3d as o3d
import numpy as np
import os
import pymeshfix

from src.controller.geometries_controller import GeometriesController
from src.object.shape import Shape


class Remesher:
    @staticmethod
    def remesh_shape(shape: Shape):
        shape.geometries.point_cloud = shape.geometries.mesh.sample_points_poisson_disk(10000)
        shape.geometries.mesh.create_from_point_cloud_poisson(shape.geometries.point_cloud)

    @staticmethod
    def fill_holes(shape: Shape):
        if shape.geometries.mesh.is_watertight():
            return

        tin = pymeshfix._meshfix.PyTMesh()
        tin.load_array(shape.geometries.mesh.vertices, shape.geometries.mesh.triangles)
        print('There are {:d} boundaries'.format(tin.boundaries()))
        tin.fill_small_boundaries()
        # tin.clean(max_iters=10, inner_loops=3)
        print('There are {:d} boundaries'.format(tin.boundaries()))

        new_path = os.path.join(os.path.split(shape.geometries.path)[0], 'remeshed.ply')
        shape.geometries.path = new_path
        tin.save_file(new_path)

        GeometriesController.set_mesh_from_file(shape.geometries, True)
        shape.geometries.mesh.remove_duplicated_vertices()

    @staticmethod
    def reconstruct_mesh(shape: Shape):
        radii = [0.005, 0.01, 0.02, 0.04]
        GeometriesController.calculate_point_cloud_normals(shape.geometries, True)
        shape.geometries.mesh = \
            o3d.geometry.TriangleMesh().create_from_point_cloud_ball_pivoting(shape.geometries.point_cloud, o3d.utility.DoubleVector(radii))

    @staticmethod
    def remove_small_meshes(shape: Shape):
        triangle_clusters, cluster_n_triangles, cluster_area = (shape.geometries.mesh.cluster_connected_triangles())

        # Numpy arrays
        triangle_clusters = np.asarray(triangle_clusters)
        cluster_n_triangles = np.asarray(cluster_n_triangles)
        cluster_area = np.asarray(cluster_area)

        # Only keep the largest meshes
        largest_cluster_idx = cluster_n_triangles.argmax()
        triangles_to_remove = triangle_clusters != largest_cluster_idx
        shape.geometries.mesh.remove_triangles_by_mask(triangles_to_remove)


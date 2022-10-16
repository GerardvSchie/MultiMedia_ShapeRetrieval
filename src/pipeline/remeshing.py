import open3d as o3d
import numpy as np
# import pymeshfix
import os
import pymeshfix

from src.controller.geometries_controller import GeometriesController
from src.object.shape import Shape

# from pymeshfix import _meshfix


class Remesher:
    @staticmethod
    def remesh_shape(shape: Shape):
        Remesher.fill_holes(shape)
        Remesher.resample(shape)
        Remesher.reconstruct_mesh(shape)

        is_watertight = shape.geometries.mesh.is_watertight()
        print('before:', shape.features.mesh_features.is_watertight, 'after:', is_watertight)

    @staticmethod
    def resample(shape: Shape):
        GeometriesController.calculate_mesh(shape.geometries)
        shape.geometries.point_cloud = shape.geometries.mesh.sample_points_poisson_disk(5000)

    @staticmethod
    def fill_holes(shape: Shape):
        if shape.geometries.mesh.is_watertight():
            return

        tin = pymeshfix._meshfix.PyTMesh()
        tin.load_array(shape.geometries.mesh.vertices, shape.geometries.mesh.triangles)

        # tin = pymeshfix.PyTMesh()
        # tin.load_file(shape.geometries.path)

        print('There are {:d} boundaries'.format(tin.boundaries()))
        tin.fill_small_boundaries()
        tin.clean(max_iters=10, inner_loops=3)
        print('There are {:d} boundaries'.format(tin.boundaries()))

        new_path = os.path.join(os.path.split(shape.geometries.path)[0], 'remeshed.ply')
        shape.geometries.path = new_path
        tin.save_file(new_path)

        GeometriesController.set_mesh_from_file(shape.geometries, True)
        shape.geometries.mesh.remove_duplicated_vertices()

    # @staticmethod
    # def merge_boundaries(shape: Shape):
    #     tin = _meshfix.PyTMesh()
    #     tin.load_file(shape.geometries.path)
    #     # tin = pymeshfix.PyTMesh()
    #     # tin.load_file(shape.geometries.path)
    #
    #     print('Nr: Boundaries', tin.boundaries())
    #     tin.join_closest_components()
    #
    #     new_path = os.path.join(os.path.split(shape.geometries.path)[0], 'merged.ply')
    #     shape.geometries.path = new_path
    #     tin.save_file(new_path)

    @staticmethod
    def reconstruct_mesh(shape: Shape):
        radii = [0.005, 0.01, 0.02, 0.04]
        GeometriesController.calculate_point_cloud_normals(shape.geometries, True)
        shape.geometries.mesh = \
            shape.geometries.mesh.create_from_point_cloud_ball_pivoting(shape.geometries.point_cloud, o3d.utility.DoubleVector(radii))

        if shape.geometries.mesh.is_watertight():
            return

        Remesher.fill_holes(shape)

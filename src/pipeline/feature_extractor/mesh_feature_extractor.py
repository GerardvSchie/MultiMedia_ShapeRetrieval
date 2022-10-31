import logging
import math
import time

import open3d as o3d
import numpy as np
from numpy.linalg import norm

from src.object.features.mesh_features import MeshFeatures


class MeshFeatureExtractor:
    @staticmethod
    def extract_convex_hull_features(mesh: o3d.geometry.TriangleMesh, mesh_features: MeshFeatures, force_recompute=False) -> bool:
        if not mesh:
            logging.warning("Cannot extract any features without mesh")
            return False

        return MeshFeatureExtractor.extract_features(mesh, mesh_features, force_recompute)

    @staticmethod
    # Only extract the features that are not yet set with values in the shape
    def extract_features(mesh: o3d.geometry.TriangleMesh, mesh_features: MeshFeatures, force_recompute=False) -> bool:
        if not mesh:
            logging.warning("Cannot extract any features without mesh")
            return False

        computed_features = [
            MeshFeatureExtractor.number_of_vertices(mesh, mesh_features, force_recompute),
            MeshFeatureExtractor.number_of_faces(mesh, mesh_features, force_recompute),
            MeshFeatureExtractor.calculate_surface_area(mesh, mesh_features, force_recompute),
            MeshFeatureExtractor.calculate_volume(mesh, mesh_features, force_recompute),
        ]

        return any(computed_features)

    @staticmethod
    def number_of_vertices(mesh: o3d.geometry.TriangleMesh, mesh_features: MeshFeatures, force_recompute=False) -> bool:
        if mesh_features.nr_vertices and not force_recompute:
            return False

        if mesh:
            nr_points = len(mesh.vertices)
        else:
            logging.warning("Cannot give number of vertices without point cloud and mesh")
            return False

        mesh_features.nr_vertices = nr_points
        return True

    @staticmethod
    def number_of_faces(mesh: o3d.geometry.TriangleMesh, mesh_features: MeshFeatures, force_recompute=False) -> bool:
        if mesh_features.nr_faces and not force_recompute:
            return False

        if mesh:
            nr_faces = len(mesh.triangles)
        else:
            logging.warning("Cannot give number of faces without mesh")
            return False

        mesh_features.nr_faces = nr_faces
        return True

    @staticmethod
    def calculate_surface_area(mesh: o3d.geometry.TriangleMesh, mesh_features: MeshFeatures, force_recompute=False) -> bool:
        if not math.isinf(mesh_features.surface_area) and not force_recompute:
            return False

        if mesh:
            surface_area = mesh.get_surface_area()
        else:
            logging.warning("Cannot give surface area without mesh")
            return False

        mesh_features.surface_area = surface_area
        return True

    @staticmethod
    def calculate_volume(mesh: o3d.geometry.TriangleMesh, mesh_features: MeshFeatures, force_recompute=False) -> bool:
        if not math.isinf(mesh_features.volume) and not force_recompute:
            return False

        if mesh:
            # Make sure all triangles are facing the same direction
            # Does not use Open3D volume implementation since it may not be watertight
            mesh.orient_triangles()
            volume = MeshFeatureExtractor.np_volume(mesh)
        else:
            logging.warning("Cannot calculate volume without mesh")
            return False

        mesh_features.volume = volume
        return True

    @staticmethod
    def np_surface_area(mesh: o3d.geometry.TriangleMesh) -> float:
        data = []
        points = np.asarray(mesh.vertices)
        for triangle in mesh.triangles:
            a = points[triangle[0]]
            b = points[triangle[1]]
            c = points[triangle[2]]
            data.append([a, b, c])

        data = np.array(data)
        vecsAB = data[:, 0] - data[:, 1]
        vecsAC = data[:, 0] - data[:, 2]

        dots = np.cross(vecsAB, vecsAC)
        norm = np.linalg.norm(dots, axis=1)
        area = np.sum(norm) / 2
        return area

    @staticmethod
    def np_volume(mesh: o3d.geometry.TriangleMesh) -> float:
        data = []
        points = np.asarray(mesh.vertices)
        for triangle in mesh.triangles:
            a = points[triangle[0]]
            b = points[triangle[1]]
            c = points[triangle[2]]
            data.append([a, b, c])

        data = np.array(data)

        crosses = np.cross(data[:, 0], data[:, 1])
        form = crosses * data[:, 2]
        volume = np.abs(np.sum(form)) / 6
        return volume

import logging
import math
import time

import open3d as o3d
import numpy as np
from numpy.linalg import norm

from src.object.features.mesh_features import MeshFeatures


class MeshFeatureExtractor:
    @staticmethod
    def extract_convex_hull_features(mesh: o3d.geometry.TriangleMesh, point_cloud: o3d.geometry.PointCloud, mesh_features: MeshFeatures, force_recompute=False):
        if not mesh and not point_cloud:
            logging.warning("Cannot extract any features without mesh and point cloud")
            return

        MeshFeatureExtractor.extract_features(mesh, point_cloud, mesh_features, force_recompute)

    @staticmethod
    # Only extract the features that are not yet set with values in the shape
    def extract_features(mesh: o3d.geometry.TriangleMesh, point_cloud: o3d.geometry.PointCloud, mesh_features: MeshFeatures, force_recompute=False):
        if not mesh and not point_cloud:
            logging.warning("Cannot extract any features without mesh and point cloud")
            return

        MeshFeatureExtractor.number_of_vertices(mesh, point_cloud, mesh_features, force_recompute)

        if mesh:
            MeshFeatureExtractor.number_of_faces(mesh, mesh_features, force_recompute)
            MeshFeatureExtractor.calculate_surface_area(mesh, mesh_features, force_recompute)
            MeshFeatureExtractor.calculate_volume(mesh, mesh_features, force_recompute)
        else:
            logging.warning("Could not extract some mesh features since mesh was missing")

    @staticmethod
    def number_of_vertices(mesh: o3d.geometry.TriangleMesh, point_cloud: o3d.geometry.PointCloud, mesh_features: MeshFeatures, force_recompute=False) -> None:
        if mesh_features.nr_vertices and not force_recompute:
            return

        if point_cloud:
            nr_points = len(point_cloud.points)
        elif mesh:
            nr_points = len(mesh.vertices)
        else:
            logging.warning("Cannot give number of vertices without point cloud and mesh")
            return

        mesh_features.nr_vertices = nr_points

    @staticmethod
    def number_of_faces(mesh: o3d.geometry.TriangleMesh, mesh_features: MeshFeatures, force_recompute=False) -> None:
        if mesh_features.nr_faces and not force_recompute:
            return

        if mesh:
            nr_faces = len(mesh.triangles)
        else:
            logging.warning("Cannot give number of faces without mesh")
            return

        mesh_features.nr_faces = nr_faces

    @staticmethod
    def calculate_surface_area(mesh: o3d.geometry.TriangleMesh, mesh_features: MeshFeatures, force_recompute=False) -> None:
        if not math.isinf(mesh_features.surface_area) and not force_recompute:
            return

        if mesh:
            surface_area = mesh.get_surface_area()
        else:
            logging.warning("Cannot give surface area without mesh")
            return

        mesh_features.surface_area = surface_area

    @staticmethod
    def calculate_volume(mesh: o3d.geometry.TriangleMesh, mesh_features: MeshFeatures, force_recompute=False) -> None:
        if not math.isinf(mesh_features.volume) and not force_recompute:
            return

        if mesh:
            # Make sure all triangles are facing the same direction
            # Does not use Open3D volume implementation since it may not be watertight
            mesh.orient_triangles()
            volume = MeshFeatureExtractor.np_volume(mesh)
        else:
            logging.warning("Cannot calculate volume without mesh")
            return

        mesh_features.volume = volume

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

    @staticmethod
    def calculate_angle_3_vertices(mesh: o3d.geometry.TriangleMesh, point_cloud: o3d.geometry.PointCloud, mesh_features: MeshFeatures, force_recompute=False) -> None:
        if not math.isinf(mesh_features.eccentricity) and not force_recompute:
            return

        # Don't yet use
        return

        # Computed over the point cloud
        if point_cloud:
            points = np.asarray(point_cloud.points)
        elif mesh:
            points = np.asarray(mesh.vertices)
        else:
            logging.warning("Cannot compute angle between points without mesh or point cloud")
            return

        for _ in range(5000):
            indices = np.random.choice(points.shape[0], 3, replace=False)
            a = points[indices[0], :]
            b = points[indices[1], :]
            c = points[indices[2], :]

            ba = a - b
            bc = c - b

            cosine_numerator = np.sum(ba * bc)
            cosine_denominator_1 = np.linalg.norm(ba)
            cosine_denominator_2 = np.linalg.norm(bc)
            cosine_angle = cosine_numerator / (cosine_denominator_1 * cosine_denominator_2)
            angles = np.arccos(cosine_angle)
            degree_angles = np.rad2deg(angles)

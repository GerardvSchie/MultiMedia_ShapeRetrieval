import logging
import math
import open3d as o3d
import numpy as np
from numpy.linalg import norm
import sys
import time

from src.object.features.mesh_features import MeshFeatures
from src.pipeline.normalization import Normalizer


class MeshFeatureExtractor:
    @staticmethod
    def extract_convex_hull_features(mesh: o3d.geometry.TriangleMesh, point_cloud: o3d.geometry.PointCloud, mesh_features: MeshFeatures, force_recompute=False):
        if not mesh and not point_cloud:
            logging.warning("Cannot extract any features without mesh and point cloud")
            return

        MeshFeatureExtractor.calculate_diameter(mesh, point_cloud, mesh_features, force_recompute)
        MeshFeatureExtractor.extract_features(mesh, point_cloud, mesh_features, force_recompute)

    @staticmethod
    # Only extract the features that are not yet set with values in the shape
    def extract_features(mesh: o3d.geometry.TriangleMesh, point_cloud: o3d.geometry.PointCloud, mesh_features: MeshFeatures, force_recompute=False):
        if not mesh and not point_cloud:
            logging.warning("Cannot extract any features without mesh and point cloud")
            return

        # MeshFeatureExtractor.calculate_angle_3_vertices(mesh, point_cloud, mesh_features, force_recompute)
        MeshFeatureExtractor.number_of_vertices(mesh, point_cloud, mesh_features, force_recompute)
        MeshFeatureExtractor.calculate_eccentricity(mesh, point_cloud, mesh_features, force_recompute)

        if mesh:
            MeshFeatureExtractor.is_watertight(mesh, mesh_features, force_recompute)
            MeshFeatureExtractor.number_of_faces(mesh, mesh_features, force_recompute)
            MeshFeatureExtractor.calculate_surface_area(mesh, mesh_features, force_recompute)
            MeshFeatureExtractor.calculate_volume(mesh, mesh_features, force_recompute)
            MeshFeatureExtractor.calculate_compactness(mesh, mesh_features, force_recompute)
            MeshFeatureExtractor.calculate_sphericity(mesh, mesh_features, force_recompute)
        else:
            logging.warning("Could not extract some mesh features since mesh was missing")

    @staticmethod
    def is_watertight(mesh: o3d.geometry.TriangleMesh, mesh_features: MeshFeatures, force_recompute=False) -> None:
        if mesh_features.is_watertight is not None and not force_recompute:
            return

        if not mesh:
            logging.warning("Cannot compute whether it is water tight without mesh")
            return

        mesh_features.is_watertight = mesh.is_watertight()

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
            if mesh.is_watertight():
                volume = mesh.get_volume()
            else:
                logging.warning("Could not calculate volume, mesh not watertight")
                return
        else:
            logging.warning("Cannot calculate volume without mesh")
            return

        mesh_features.volume = volume

    @staticmethod
    def calculate_diameter(mesh: o3d.geometry.TriangleMesh, point_cloud: o3d.geometry.PointCloud, mesh_features: MeshFeatures, force_recompute=False) -> None:
        if not math.isinf(mesh_features.diameter) and not force_recompute:
            return

        if point_cloud:
            points = point_cloud.points
        elif mesh:
            points = mesh.vertices
        else:
            logging.warning('Cannot compute diameter without mesh or point cloud')
            return

        points = np.asarray(points)

        if len(points) < 2:
            logging.warning('Cannot compute diameter with less than 2 points')
            return

        max_squared_distance = -math.inf

        for point_a_index in range(len(points)):
            point_a = points[point_a_index]
            for point_b_index in range(point_a_index + 1, len(points)):
                point_b = points[point_b_index]
                squared_distance = np.sum(np.power(point_a - point_b, 2))
                if squared_distance > max_squared_distance:
                    max_squared_distance = squared_distance

        max_diameter = np.sqrt(max_squared_distance)
        mesh_features.diameter = max_diameter

    @staticmethod
    def calculate_compactness(mesh: o3d.geometry.TriangleMesh, mesh_features: MeshFeatures, force_recompute=False) -> None:
        if not math.isinf(mesh_features.compactness) and not force_recompute:
            return

        if not mesh:
            logging.warning('Could not compute compactness without mesh')
            return

        MeshFeatureExtractor.calculate_surface_area(mesh, mesh_features, force_recompute)
        MeshFeatureExtractor.calculate_volume(mesh, mesh_features, force_recompute)

        if math.isinf(mesh_features.volume):
            logging.warning('Could not compute volume without water tight mesh')

        compactness = np.power(mesh_features.surface_area, 3) / (36 * math.pi * np.power(mesh_features.volume, 2))
        mesh_features.compactness = compactness

    @staticmethod
    def calculate_sphericity(mesh: o3d.geometry.TriangleMesh, mesh_features: MeshFeatures, force_recompute=False) -> None:
        if not math.isinf(mesh_features.sphericity) and not force_recompute:
            return

        if not mesh:
            logging.warning('Could not compute sphericity without mesh')
            return

        MeshFeatureExtractor.calculate_compactness(mesh, mesh_features, force_recompute)
        if math.isinf(mesh_features.compactness):
            logging.warning('Could not compute sphericity without compactness')

        mesh_features.sphericity = 1 / mesh_features.compactness

    @staticmethod
    def calculate_eccentricity(mesh: o3d.geometry.TriangleMesh, point_cloud: o3d.geometry.PointCloud, mesh_features: MeshFeatures, force_recompute=False) -> None:
        if not math.isinf(mesh_features.eccentricity) and not force_recompute:
            return

        # Computed over the point cloud
        if point_cloud:
            eigenvalues_eigenvectors = Normalizer.get_eigenvalues_and_eigenvectors(point_cloud)
        elif mesh:
            eigenvalues_eigenvectors = Normalizer.get_eigenvalues_and_eigenvectors(
                o3d.geometry.PointCloud(mesh.vertices))
        else:
            logging.warning("Cannot compute alignment without mesh or point cloud")
            return

        # Return the average dot product
        eccentricity = np.abs(eigenvalues_eigenvectors[0][0]) / np.abs(eigenvalues_eigenvectors[2][0])
        mesh_features.eccentricity = eccentricity

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

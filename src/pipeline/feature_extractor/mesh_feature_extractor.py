import logging
import math
import open3d as o3d

from src.object.features.mesh_features import MeshFeatures


class MeshFeatureExtractor:
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
            if mesh.is_watertight():
                volume = mesh.get_volume()
            else:
                logging.warning("Could not calculate volume, mesh not watertight")
                return
        else:
            logging.warning("Cannot calculate volume without mesh")
            return

        mesh_features.volume = volume

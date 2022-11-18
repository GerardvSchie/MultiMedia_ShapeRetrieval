import logging
import math
import open3d as o3d
import numpy as np

from src.object.features.mesh_features import MeshFeatures


class MeshFeatureExtractor:
    @staticmethod
    # Only extract the features that are not yet set with values in the shape
    def extract_features(mesh: o3d.geometry.TriangleMesh, mesh_features: MeshFeatures, force_recompute=False) -> bool:
        """Extract all mesh features, this could also be a convex hull

        :param mesh: Mesh to
        :param mesh_features:
        :param force_recompute:
        :return: The features to c
        """
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
        """Get the number of vertices of the given mesh

        :param mesh: Mesh to compute the number of vertices of
        :param mesh_features: Object to save the result in
        :param force_recompute: Whether to force recomputing this feature
        :return: Whether the feature got recomputed
        """
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
        """Get the number of faces of the given mesh

        :param mesh: Mesh to compute the number of cells of
        :param mesh_features: Object to save the result in
        :param force_recompute: Whether to force recomputing this feature
        :return: Whether the feature got recomputed
        """
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
        """Get the total surface area of the mesh

        :param mesh: Mesh to compute the surface area of
        :param mesh_features: Object to save the result in
        :param force_recompute: Whether to force recomputing this feature
        :return: Whether the feature got recomputed
        """
        if not math.isinf(mesh_features.surface_area) and not force_recompute:
            return False

        # Can only compute if mesh is loaded
        if mesh:
            surface_area = mesh.get_surface_area()
        else:
            logging.warning("Cannot give surface area without mesh")
            return False

        mesh_features.surface_area = surface_area
        return True

    @staticmethod
    def calculate_volume(mesh: o3d.geometry.TriangleMesh, mesh_features: MeshFeatures, force_recompute=False) -> bool:
        """Get the total volume of the mesh, uses numpy to speed up calculations compared to Open3D

        :param mesh: Mesh to compute the volume of
        :param mesh_features: Object to save the result in
        :param force_recompute: Whether to force recomputing this feature
        :return: Whether the feature got recomputed
        """
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
    def np_volume(mesh: o3d.geometry.TriangleMesh) -> float:
        """Use numpy to compute the volume of the triangle mesh
        Is faster than the Open3D method and does not require the mesh to be watertight

        :param mesh: Mesh to compute the volume of
        :return: The total volume of the mesh
        """
        data = []
        points = np.asarray(mesh.vertices)

        # Fill each entry in data with the triangle coordinates
        for triangle in mesh.triangles:
            a = points[triangle[0]]
            b = points[triangle[1]]
            c = points[triangle[2]]
            data.append([a, b, c])

        # Compute the volume of the cell with the 4th vertex at the origin
        data = np.array(data)
        crosses = np.cross(data[:, 0], data[:, 1])
        form = crosses * data[:, 2]
        volume = np.abs(np.sum(form)) / 6
        return volume

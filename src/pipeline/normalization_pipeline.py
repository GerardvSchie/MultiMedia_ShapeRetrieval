import os
import open3d as o3d

from src.pipeline.compute_descriptors import compute_descriptors
from src.controller.geometries_controller import GeometriesController
from src.pipeline.feature_extractor.normalization_feature_extractor import NormalizationFeatureExtractor
from src.object.shape import Shape
from src.pipeline.feature_extractor.shape_feature_extractor import ShapeFeatureExtractor
from src.database.reader import DatabaseReader
from src.pipeline.normalization import Normalizer
from src.vertex_normalization import simplifyMesh
from src.util.configs import *


class NormalizationPipeline:
    def __init__(self):
        # Load all shape features
        self.shape_features = DatabaseReader.read_features_paths([
            os.path.join(DATABASE_ORIGINAL_DIR, DATABASE_FEATURES_FILENAME),
            os.path.join(DATABASE_REFINED_DIR, DATABASE_FEATURES_FILENAME)
        ])

        self.shape_descriptors = DatabaseReader.read_descriptors(
            os.path.join(DATABASE_REFINED_DIR, DATABASE_DESCRIPTORS_FILENAME))

    def normalize_shape(self, path: str) -> Shape:
        # Create shape object
        shape = Shape(os.path.relpath(path))

        # Create point cloud
        if shape.geometries.path.endswith(FILENAME_ORIGINAL):
            new_path = os.path.join(os.path.split(shape.geometries.path)[0], FILENAME_NORMALIZED_PCD)

            # Path already exists, set path of shape to point cloud
            if os.path.exists(new_path):
                shape.geometries.path = new_path
            else:
                GeometriesController.set_mesh_from_file(shape.geometries)
                shape.geometries.point_cloud = shape.geometries.mesh.sample_points_poisson_disk(NR_VERTICES)

                # When normalization is successful
                if Normalizer.normalize_shape(shape):
                    shape.save_pcd(new_path)
                    shape.geometries.path = new_path

        # Create high resolution mesh of pcd
        if shape.geometries.path.endswith(FILENAME_NORMALIZED_PCD):
            new_path = os.path.join(os.path.split(shape.geometries.path)[0], FILENAME_NORMALIZED_PLY)

            if not os.path.exists(new_path):
                point_cloud: o3d.geometry.PointCloud = o3d.io.read_point_cloud(shape.geometries.path)
                point_cloud.estimate_normals()
                point_cloud.orient_normals_consistent_tangent_plane(10)

                mesh, _ = o3d.geometry.TriangleMesh().create_from_point_cloud_poisson(point_cloud)
                mesh: o3d.geometry.TriangleMesh = mesh
                o3d.io.write_triangle_mesh(new_path, mesh)

            shape.set_new_ply_path(new_path)

        if shape.geometries.path.endswith(FILENAME_NORMALIZED_PLY):
            new_path = os.path.join(os.path.split(shape.geometries.path)[0], FILENAME_REFINED)
            if not os.path.exists(new_path):
                refined_mesh, _ = simplifyMesh(shape.geometries.path, NR_VERTICES)
                refined_mesh.save_current_mesh(new_path)

            shape.set_new_ply_path(new_path)

        # Use pre-computed features and descriptors if present
        if self.shape_features.__contains__(shape.geometries.path):
            shape.features = self.shape_features[shape.geometries.path]
        if self.shape_descriptors.__contains__(shape.geometries.path):
            shape.descriptors = self.shape_descriptors[shape.geometries.path]

        # First extract the normalization features from the pcd
        if shape.features.normalization_features.misses_values():
            pcd_name = os.path.join(os.path.split(shape.geometries.path)[0], FILENAME_NORMALIZED_PCD)
            normalized_point_cloud = o3d.io.read_point_cloud(pcd_name)
            NormalizationFeatureExtractor.extract_features(normalized_point_cloud,
                                                           shape.features.normalization_features)

        # All other features can be computed afterwards
        ShapeFeatureExtractor.extract_all_shape_features(shape)
        compute_descriptors(shape)

        return shape

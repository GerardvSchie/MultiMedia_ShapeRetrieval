from src.pipeline.compute_descriptors import compute_descriptors
from src.controller.geometries_controller import GeometriesController
from src.object.shape import Shape
from src.pipeline.feature_extractor.shape_feature_extractor import ShapeFeatureExtractor
from src.database.reader import FeatureDatabaseReader
from src.pipeline.normalization import Normalizer
from src.util.configs import *


class NormalizationPipeline:
    def __init__(self):
        # Load all shape features
        self.shape_features = FeatureDatabaseReader.read_features_paths([
            os.path.join(DATABASE_ORIGINAL_DIR, DATABASE_FEATURES_FILENAME),
            os.path.join(DATABASE_NORMALIZED_DIR, DATABASE_FEATURES_FILENAME)
        ])

        self.shape_descriptors = FeatureDatabaseReader.read_descriptors(
            os.path.join(DATABASE_NORMALIZED_DIR, DATABASE_DESCRIPTORS_FILENAME))

    def normalize_shape(self, path: str) -> Shape:
        # Create shape object
        shape = Shape(os.path.relpath(path))

        # Create point cloud and resample
        if shape.geometries.path.endswith(FILENAME_ORIGINAL):
            new_path = os.path.join(os.path.split(shape.geometries.path)[0], FILENAME_NORMALIZED_PCD)

            dir_path = os.path.split(shape.geometries.path)[0]
            normalized_pcd_path = os.path.join(dir_path, FILENAME_NORMALIZED_PCD)
            normalized_ply_path = os.path.join(dir_path, FILENAME_NORMALIZED_PLY)

            # Path already exists, set path of shape to point cloud
            if os.path.exists(normalized_pcd_path) and os.path.exists(normalized_ply_path):
                shape.set_new_ply_path(normalized_ply_path)
            else:
                GeometriesController.set_mesh_from_file(shape.geometries)
                shape.geometries.point_cloud = shape.geometries.mesh.sample_points_poisson_disk(NR_VERTICES, seed=0)

                # When normalization is successful
                if Normalizer.normalize_shape(shape):
                    shape.save_pcd(normalized_pcd_path)
                    shape.save_ply(normalized_ply_path)
                    shape.geometries.path = new_path

            shape.set_new_ply_path(normalized_ply_path)

        # Use pre-computed features and descriptors if present
        if self.shape_features.__contains__(shape.geometries.path):
            shape.features = self.shape_features[shape.geometries.path]
        if self.shape_descriptors.__contains__(shape.geometries.path):
            shape.descriptors = self.shape_descriptors[shape.geometries.path]

        # Load mesh and PCD from separate files
        GeometriesController.set_mesh_from_file(shape.geometries)
        GeometriesController.set_pcd_from_file(shape.geometries)

        # All other features can be computed afterwards
        ShapeFeatureExtractor.extract_all_shape_features(shape)
        compute_descriptors(shape)

        return shape

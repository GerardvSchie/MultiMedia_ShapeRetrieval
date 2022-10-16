import os
from tqdm import tqdm

# Needed to fix ModuleNotFoundError when importing src.util.logger.
from src.object.features.shape_features import ShapeFeatures
from src.pipeline.feature_extractor.mesh_feature_extractor import MeshFeatureExtractor

directoryContainingCurrentFile = os.path.dirname(__file__)
repoDirectory = os.path.dirname(directoryContainingCurrentFile)

# Add repo to list of possible paths
import sys
sys.path.append(repoDirectory)

from src.controller.geometries_controller import GeometriesController
from src.pipeline.feature_extractor.normalization_feature_extractor import NormalizationFeatureExtractor
import src.util.logger as logger
from src.object.shape import Shape
from src.pipeline.feature_extractor.shape_feature_extractor import ShapeFeatureExtractor
import src.util.plot
from src.database.writer import DatabaseWriter
from src.database.reader import DatabaseReader
from src.util.io import check_working_dir
from src.pipeline.normalization import Normalizer
from src.plot.feature_distribution import FeatureDistributionPlotter


def read_original_shapes() -> [Shape]:
    shape_list = []

    # Walk through labeledDB directory
    for sub_item in os.scandir(os.path.join("data", "LabeledDB_new")):
        if not sub_item.is_dir():
            continue

        for item in os.scandir(sub_item.path):
            if item.is_dir():
                continue

            if not item.path.endswith('.off'):
                continue

            # Database depends on relative paths
            shape = Shape(os.path.relpath(item.path))
            shape_list.append(shape)

    return shape_list


def read_normalized_shapes() -> [Shape]:
    shape_list = []

    # Walk through labeledDB directory
    for category in os.scandir(os.path.join("data", "LabeledDB_new")):
        if not category.is_dir():
            continue

        for number in os.scandir(category.path):
            if not number.is_dir():
                continue

            for item in os.scandir(number.path):
                if item.is_dir() or item.name != 'normalized.ply':
                    continue

                # Database depends on relative paths
                shape = Shape(os.path.relpath(item.path))
                shape_list.append(shape)

    return shape_list


def add_shape_features(shape_list: [Shape]) -> None:
    features_data = DatabaseReader.read_all_shape_features()

    for shape in shape_list:
        if shape.geometries.path in features_data:
            shape.features = features_data[shape.geometries.path]


def normalize_and_save_shape(shape: Shape):
    # Calculate
    GeometriesController.calculate_mesh(shape.geometries)
    GeometriesController.calculate_point_cloud(shape.geometries)
    GeometriesController.calculate_aligned_bounding_box(shape.geometries)

    Normalizer.normalize_shape(shape)
    new_path = os.path.join(os.path.split(shape.geometries.path)[0], 'normalized.ply')
    shape.geometries.path = new_path
    shape.save(shape.geometries.path)

    GeometriesController.calculate_point_cloud(shape.geometries, True)
    GeometriesController.calculate_aligned_bounding_box(shape.geometries, True)
    NormalizationFeatureExtractor.extract_features(shape.geometries.mesh, shape.geometries.point_cloud, shape.geometries.axis_aligned_bounding_box, shape.features.normalization_features, True)


def write_shape_features(shape_collection: [Shape]) -> None:
    DatabaseWriter.write_all_shape_features(shape_collection)


def plot_feature_data(shape_collection: [Shape]) -> None:
    shape_features = [shape.features for shape in shape_collection]
    FeatureDistributionPlotter.plot_features(shape_features)


def main():
    # Offline computed features
    # shape_list = read_normalized_shapes()
    shape_list = read_original_shapes()
    add_shape_features(shape_list)

    for shape in tqdm(shape_list):
        GeometriesController.calculate_mesh(shape.geometries)
        MeshFeatureExtractor.is_watertight(shape.geometries.mesh, shape.features.mesh_features)

    # How to then change the shape
    # for shape in shape_list:
    #     normalize_and_save_shape(shape)

    # GeometriesController.calculate_mesh(shape.geometries)
    # GeometriesController.calculate_point_cloud(shape.geometries)
    # GeometriesController.calculate_aligned_bounding_box(shape.geometries)
    # normalize_and_save_shape(shape)
    # GeometriesController.calculate_point_cloud(shape.geometries, True)
    # GeometriesController.calculate_aligned_bounding_box(shape.geometries, True)
    # NormalizationFeatureExtractor.extract_features(shape.geometries.mesh, shape.geometries.point_cloud, shape.geometries.axis_aligned_bounding_box, shape.features.normalization_features, True)
    # print('done extracting')

    # Disable additional feature extraction, meshes are not watertight
    # ShapeFeatureExtractor.extract_axis_aligned_bounding_box(shape)
    # ShapeFeatureExtractor.extract_mesh_features(shape)
    # ShapeFeatureExtractor.extract_convex_hull_features(shape)
    # ShapeFeatureExtractor.extract_normalization_features(shape)
    # ShapeFeatureExtractor.extract_axis_aligned_bounding_box(shape)
    # ShapeFeatureExtractor.extract_normalization_features(shape)

    # Collect the paths to the Shapes too for refinement, if needed.
    # shapePaths = [shape.geometries.path for shape in shape_collection]
    # src.util.plot.plot_features([shape.features for shape in shape_collection], shapePaths)

    plot_feature_data(shape_list)
    # write_shape_features(shape_list)


# Example loads an .off and .ply file
if __name__ == '__main__':
    logger.initialize()
    check_working_dir()
    main()
    print("run complete")

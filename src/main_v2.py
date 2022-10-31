import os
from tqdm import tqdm
import sys
import open3d as o3d
from matplotlib import pyplot as plt
import numpy as np
import matplotlib

from pipeline.feature_extractor.shape_properties_extractor import ShapeProps

# Needed to fix ModuleNotFoundError when importing src.util.logger.
directoryContainingCurrentFile = os.path.dirname(__file__)
repoDirectory = os.path.dirname(directoryContainingCurrentFile)

# Add repo to list of possible paths
sys.path.append(repoDirectory)

import src.util.logger as logger

from src.pipeline.normalize_descriptors import normalize_descriptors
from src.plot.descriptor_distribution import DescriptorDistributionPlotter
from src.plot.distance_matrix import DistanceMatrixPlotter
from src.pipeline.compute_descriptors import compute_descriptors
from src.controller.geometries_controller import GeometriesController
from src.pipeline.feature_extractor.normalization_feature_extractor import NormalizationFeatureExtractor
from src.object.shape import Shape
from src.pipeline.feature_extractor.shape_feature_extractor import ShapeFeatureExtractor
from src.database.writer import DatabaseWriter
from src.database.reader import DatabaseReader
from src.util.io import check_working_dir
from src.pipeline.normalization import Normalizer
from src.plot.feature_distribution import FeatureDistributionPlotter
from src.util.configs import *
from src.plot.io import save_plt


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

    add_shape_features(shape_list, os.path.join(DATABASE_ORIGINAL_DIR, DATABASE_FEATURES_FILENAME))
    add_shape_descriptors(shape_list, os.path.join(DATABASE_ORIGINAL_DIR, DATABASE_DESCRIPTORS_FILENAME))
    return shape_list


def add_shape_features(shape_list: [Shape], path: str) -> None:
    features_data = DatabaseReader.read_features(path)

    for shape in shape_list:
        if shape.geometries.path in features_data:
            shape.features = features_data[shape.geometries.path]


def add_shape_descriptors(shape_list: [Shape], path: str) -> None:
    descriptors_data = DatabaseReader.read_descriptors(path)

    for shape in shape_list:
        if shape.geometries.path in descriptors_data:
            shape.descriptors = descriptors_data[shape.geometries.path]


def normalize_and_save_shape(shape: Shape):
    dir_path = os.path.split(shape.geometries.path)[0]
    normalized_pcd_path = os.path.join(dir_path, FILENAME_NORMALIZED_PCD)
    normalized_path = os.path.join(dir_path, FILENAME_NORMALIZED_PLY)

    if os.path.exists(normalized_pcd_path) and os.path.exists(normalized_path):
        return

    # When normalization is successful
    if Normalizer.normalize_shape(shape):
        shape.save_pcd(normalized_pcd_path)
        shape.save_ply(normalized_path)

        shape.geometries.path = normalized_path


def plot_feature_data(shape_collection: [Shape]) -> None:
    FeatureDistributionPlotter.plot_features([shape.features for shape in shape_collection])


def main():
    recompute_plots = False

    # Compute offline features
    shape_list = read_original_shapes()

    # Compute the features and descriptors
    print('\nCompute features of original shapes:\n')
    recomputed_features = []
    recomputed_descriptors = []
    for shape in tqdm(shape_list):
        recomputed_features.append(ShapeFeatureExtractor.extract_all_shape_features(shape))
        recomputed_descriptors.append(compute_descriptors(shape))

    #     print(shape.geometries.path, 'S:', shape.features.mesh_features.surface_area / np.power(shape.features.normalization_features.scale, 2), 'V:',
    #           shape.features.mesh_features.volume / np.power(shape.features.normalization_features.scale, 3))
    #
    # sys.exit()

    # Only write file if new features are computed
    if any(recomputed_features):
        DatabaseWriter.write_features(shape_list, os.path.join(DATABASE_ORIGINAL_DIR, DATABASE_FEATURES_FILENAME))
    if any(recomputed_features) or recompute_plots:
        FeatureDistributionPlotter.plot_features(PLOT_ORIGINAL_FEATURES_DIR, [shape.features for shape in shape_list])
    if any(recomputed_descriptors):
        DatabaseWriter.write_descriptors(shape_list, os.path.join(DATABASE_ORIGINAL_DIR, DATABASE_DESCRIPTORS_FILENAME))

    # Remesh shapes
    print('\n--------------\nResample shapes + normalize')
    for shape in tqdm(shape_list):
        if not shape.geometries.path.endswith(FILENAME_ORIGINAL):
            continue

        dir_path = os.path.split(shape.geometries.path)[0]
        poisson_pcd_path = os.path.join(dir_path, FILENAME_NORMALIZED_PCD)
        normalized_path = os.path.join(dir_path, FILENAME_NORMALIZED_PLY)

        if os.path.exists(poisson_pcd_path) and os.path.exists(normalized_path):
            continue

        GeometriesController.set_mesh_from_file(shape.geometries)
        shape.geometries.point_cloud = shape.geometries.mesh.sample_points_poisson_disk(NR_VERTICES, seed=0)

        # When normalization is successful
        if Normalizer.normalize_shape(shape):
            shape.save_pcd(poisson_pcd_path)
            shape.save_ply(normalized_path)

            shape.set_new_ply_path(normalized_path)

    sys.exit()

    add_shape_features(shape_list, os.path.join(DATABASE_NORMALIZED_DIR, DATABASE_FEATURES_FILENAME))
    add_shape_descriptors(shape_list, os.path.join(DATABASE_NORMALIZED_DIR, DATABASE_DESCRIPTORS_FILENAME))

    print('\nCompute features of normalized shapes:\n')
    recomputed_features = []
    recomputed_descriptors = []
    for shape in tqdm(shape_list):
        # First extract the normalization features from the pcd
        if shape.features.normalization_features.misses_values():
            pcd_name = os.path.join(os.path.split(shape.geometries.path)[0], FILENAME_NORMALIZED_PCD)
            normalized_point_cloud = o3d.io.read_point_cloud(pcd_name)
            recomputed_features.append(NormalizationFeatureExtractor.extract_features(normalized_point_cloud, shape.features.normalization_features))

        # All other features can be computed afterwards
        recomputed_features.append(ShapeFeatureExtractor.extract_all_shape_features(shape))
        recomputed_descriptors.append(compute_descriptors(shape))

    if any(recomputed_features):
        DatabaseWriter.write_features(shape_list, os.path.join(DATABASE_NORMALIZED_DIR, DATABASE_FEATURES_FILENAME))
        FeatureDistributionPlotter.plot_features(DATABASE_NORMALIZED_DIR, [shape.features for shape in shape_list])
    if any(recomputed_descriptors):
        DatabaseWriter.write_descriptors(shape_list, os.path.join(DATABASE_NORMALIZED_DIR, DATABASE_DESCRIPTORS_FILENAME))
        normalize_descriptors(os.path.join(DATABASE_NORMALIZED_DIR, DATABASE_DESCRIPTORS_FILENAME))

    if any(recomputed_descriptors) or recompute_plots:
        DescriptorDistributionPlotter.plot_features(PLOT_REFINED_DESCRIPTORS_DIR, [shape.descriptors for shape in shape_list])
        normalized_descriptors = DatabaseReader.read_descriptors(os.path.join(DATABASE_REFINED_DIR, DATABASE_NORMALIZED_DESCRIPTORS_FILENAME))
        DescriptorDistributionPlotter.plot_features(PLOT_NORMALIZED_DESCRIPTORS_DIR, list(normalized_descriptors.values()))

        DistanceMatrixPlotter.plot(normalized_descriptors)


# def main():
#
#     add_shape_features(shape_list, os.path.join(DATABASE_REFINED_DIR, DATABASE_FEATURES_FILENAME))
#     add_shape_descriptors(shape_list, os.path.join(DATABASE_REFINED_DIR, DATABASE_DESCRIPTORS_FILENAME))
#
#     print('\nCompute features of normalized shapes:\n')
#     recomputed_features = []
#     recomputed_descriptors = []
#     for shape in tqdm(shape_list):
#         # First extract the normalization features from the pcd
#         if shape.features.normalization_features.misses_values():
#             pcd_name = os.path.join(os.path.split(shape.geometries.path)[0], FILENAME_NORMALIZED_PCD)
#             normalized_point_cloud = o3d.io.read_point_cloud(pcd_name)
#             recomputed_features.append(NormalizationFeatureExtractor.extract_features(normalized_point_cloud, shape.features.normalization_features))
#
#         # All other features can be computed afterwards
#         recomputed_features.append(ShapeFeatureExtractor.extract_all_shape_features(shape))
#         recomputed_descriptors.append(compute_descriptors(shape))
#
#     if any(recomputed_features):
#         DatabaseWriter.write_features(shape_list, os.path.join(DATABASE_REFINED_DIR, DATABASE_FEATURES_FILENAME))
#         FeatureDistributionPlotter.plot_features(PLOT_REFINED_FEATURES_DIR, [shape.features for shape in shape_list])
#     if any(recomputed_descriptors):
#         DatabaseWriter.write_descriptors(shape_list, os.path.join(DATABASE_REFINED_DIR, DATABASE_DESCRIPTORS_FILENAME))
#         normalize_descriptors(os.path.join(DATABASE_REFINED_DIR, DATABASE_DESCRIPTORS_FILENAME))
#
#     if any(recomputed_descriptors) or recompute_plots:
#         DescriptorDistributionPlotter.plot_features(PLOT_REFINED_DESCRIPTORS_DIR, [shape.descriptors for shape in shape_list])
#         normalized_descriptors = DatabaseReader.read_descriptors(os.path.join(DATABASE_REFINED_DIR, DATABASE_NORMALIZED_DESCRIPTORS_FILENAME))
#         DescriptorDistributionPlotter.plot_features(PLOT_NORMALIZED_DESCRIPTORS_DIR, list(normalized_descriptors.values()))
#
#         DistanceMatrixPlotter.plot(normalized_descriptors)

    # plot_feature(shape_list, 'Ant')
    # plot_feature(shape_list, 'Airplane')
    # plot_feature(shape_list, 'Vase')


def plot_feature(shape_list: [Shape], category: str):
    features_list = []
    for shape in tqdm(shape_list):
        if shape.features.true_class != category:
            continue

        features = ShapeProps.shape_propertizer(shape)
        features_list.append(features)

    for feat in features_list:
        d1_features = feat["D1"]
        plt.plot((d1_features[1][0:-1] + d1_features[1][1:]) / 2, d1_features[0])

    save_plt(os.path.join(PLOT_PROPERTIES_DIR, f'd1_{category}.png'))

    for feat in features_list:
        d2_features = feat["D2"]
        plt.plot((d2_features[1][0:-1] + d2_features[1][1:]) / 2, d2_features[0])

    save_plt(os.path.join(PLOT_PROPERTIES_DIR, f'd2_{category}.png'))

    for feat in features_list:
        d3_features = feat["D3"]
        plt.plot((d3_features[1][0:-1] + d3_features[1][1:]) / 2, d3_features[0])

    save_plt(os.path.join(PLOT_PROPERTIES_DIR, f'd3_{category}.png'))

    for feat in features_list:
        a3_features = feat["A3"]
        plt.plot((a3_features[1][0:-1] + a3_features[1][1:]) / 2, a3_features[0])

    save_plt(os.path.join(PLOT_PROPERTIES_DIR, f'a3_{category}.png'))

    for feat in features_list:
        d4_features = feat["D4"]
        plt.plot((d4_features[1][0:-1] + d4_features[1][1:]) / 2, d4_features[0])
    save_plt(os.path.join(PLOT_PROPERTIES_DIR, f'd4_{category}.png'))


# Example loads an .off and .ply file
if __name__ == '__main__':
    logger.initialize()
    check_working_dir()
    matplotlib.use('Agg')
    main()
    print("run complete")

import os
from tqdm import tqdm
import sys
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

import src.plot.util

# Needed to fix ModuleNotFoundError when importing src.util.logger.
directoryContainingCurrentFile = os.path.dirname(__file__)
repoDirectory = os.path.dirname(directoryContainingCurrentFile)

# Add repo to list of possible paths
sys.path.append(repoDirectory)

import src.util.logger as logger

from src.pipeline.feature_extractor.optimized_shape_properties_extractor import ShapePropsOptimized
from src.pipeline.normalize_descriptors import normalize_descriptors
from src.pipeline.normalize_properties import normalize_properties
from src.plot.descriptor_distribution import DescriptorDistributionPlotter
from src.plot.distance_matrix import DistanceMatrixPlotter
from src.pipeline.compute_descriptors import compute_descriptors
from src.controller.geometries_controller import GeometriesController
from src.object.shape import Shape
from src.pipeline.feature_extractor.shape_feature_extractor import ShapeFeatureExtractor
from src.database.writer import DatabaseWriter
from src.database.reader import DatabaseReader
from src.util.io import check_working_dir
from src.pipeline.normalization import Normalizer
from src.plot.feature_distribution import FeatureDistributionPlotter
from src.util.configs import *
from src.plot.io import save_plt
from src.object.properties import Properties


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


def add_shape_properties(shape_list: [Shape], path: str) -> None:
    properties_data = DatabaseReader.read_properties(path)

    for shape in shape_list:
        if shape.geometries.path in properties_data:
            shape.properties = properties_data[shape.geometries.path]


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


def plot_property(shape_list: [Shape], property_name: str, x_label: str):
    prev_category = ''
    data = [shape.properties.__getattribute__(property_name) for shape in shape_list]
    for shape_index in range(len(shape_list)):
        shape = shape_list[shape_index]
        if prev_category and shape.features.true_class != prev_category:
            save_property_plot(prev_category, property_name, x_label)

        prev_category = shape.features.true_class
        bins = np.arange(0.025, 1, 0.05) * Properties.MAX[property_name]
        plt.plot(bins, data[shape_index])

    save_property_plot(prev_category, property_name, x_label)


def save_property_plot(category: str, property_name: str, x_label: str):
    src.plot.util.set_params()
    plt.title(property_name.upper() + ' distribution ' + category,
              fontdict={'fontsize': src.plot.util.BIGGER_SIZE})
    plt.ylabel('Percentage of samples')
    plt.xlabel(x_label)
    plt.ylim(0, 1)
    save_plt(os.path.join(PLOT_PROPERTIES_DIR, property_name, f'{category}.png'))


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
            shape.set_new_ply_path(normalized_path)
            continue

        GeometriesController.set_mesh_from_file(shape.geometries)
        shape.geometries.point_cloud = shape.geometries.mesh.sample_points_poisson_disk(NR_VERTICES, seed=0)

        # When normalization is successful
        if Normalizer.normalize_shape(shape):
            shape.save_pcd(poisson_pcd_path)
            shape.save_ply(normalized_path)

        shape.set_new_ply_path(normalized_path)

    add_shape_features(shape_list, os.path.join(DATABASE_NORMALIZED_DIR, DATABASE_FEATURES_FILENAME))
    add_shape_descriptors(shape_list, os.path.join(DATABASE_NORMALIZED_DIR, DATABASE_DESCRIPTORS_FILENAME))

    print('\nCompute features of normalized shapes:\n')
    recomputed_features = []
    recomputed_descriptors = []
    for shape in tqdm(shape_list):
        # All other features can be computed afterwards
        recomputed_features.append(ShapeFeatureExtractor.extract_all_shape_features(shape))
        recomputed_descriptors.append(compute_descriptors(shape))

    if any(recomputed_features):
        DatabaseWriter.write_features(shape_list, os.path.join(DATABASE_NORMALIZED_DIR, DATABASE_FEATURES_FILENAME))
        FeatureDistributionPlotter.plot_features(PLOT_REFINED_FEATURES_DIR, [shape.features for shape in shape_list])
    if any(recomputed_descriptors):
        DatabaseWriter.write_descriptors(shape_list, os.path.join(DATABASE_NORMALIZED_DIR, DATABASE_DESCRIPTORS_FILENAME))
        normalize_descriptors(os.path.join(DATABASE_NORMALIZED_DIR, DATABASE_DESCRIPTORS_FILENAME))

    if any(recomputed_descriptors) or recompute_plots:
        DescriptorDistributionPlotter.plot_features(PLOT_REFINED_DESCRIPTORS_DIR, [shape.descriptors for shape in shape_list])
        normalized_descriptors = DatabaseReader.read_descriptors(os.path.join(DATABASE_NORMALIZED_DIR, DATABASE_NORMALIZED_DESCRIPTORS_FILENAME))
        DescriptorDistributionPlotter.plot_features(PLOT_NORMALIZED_DESCRIPTORS_DIR, list(normalized_descriptors.values()))
        DistanceMatrixPlotter.plot(normalized_descriptors)

    print('\nCompute properties of shapes:\n')
    add_shape_properties(shape_list, os.path.join(DATABASE_NORMALIZED_DIR, DATABASE_PROPERTIES_FILENAME))

    recomputed_properties = []
    for shape in tqdm(shape_list):
        recomputed_properties.append(ShapePropsOptimized.shape_propertizer(shape))

    # Histograms
    if any(recomputed_properties) or True:
        DatabaseWriter.write_properties(shape_list, os.path.join(DATABASE_NORMALIZED_DIR, DATABASE_PROPERTIES_FILENAME))
        normalize_properties(os.path.join(DATABASE_NORMALIZED_DIR, DATABASE_PROPERTIES_FILENAME))

    # Distance matrices
    if any(recomputed_properties) or recompute_plots:
        plot_property(shape_list, 'd1', 'Distance to center')
        plot_property(shape_list, 'd2', 'Distance between two vertices')
        plot_property(shape_list, 'd3', 'Area of triangle')
        plot_property(shape_list, 'd4', 'Volume of tetrahedron')
        plot_property(shape_list, 'a3', 'Angle between 3 vertices')

    if any(recomputed_properties) or recompute_plots or True:
        properties = DatabaseReader.read_properties(os.path.join(DATABASE_NORMALIZED_DIR, DATABASE_NORMALIZED_PROPERTIES_FILENAME))
        DistanceMatrixPlotter.plot_properties(properties)


# Example loads an .off and .ply file
if __name__ == '__main__':
    logger.initialize()
    check_working_dir()
    matplotlib.use('Agg')
    main()
    print("run complete")

import os
from tqdm import tqdm
import sys
import matplotlib

# Needed to fix ModuleNotFoundError when importing src.util.logger.
directoryContainingCurrentFile = os.path.dirname(__file__)
repoDirectory = os.path.dirname(directoryContainingCurrentFile)

# Add repo to list of possible paths
sys.path.append(repoDirectory)

import src.util.logger as logger

from src.object.distances import Distances
from src.pipeline.feature_extractor.shape_properties_extractor import ShapePropertyExtractor
from src.pipeline.compute_distances import calc_distances
from src.plot.tsne import plot_tsne
from src.pipeline.compute_tsne import dimensionality_reduction
from src.plot.property_distribution import plot_property
from src.pipeline.normalize_descriptors import normalize_descriptors
from src.pipeline.normalize_properties import normalize_properties
from src.plot.descriptor_distribution import DescriptorDistributionPlotter
from src.plot.distance_matrix import DistanceMatrixPlotter
from src.pipeline.compute_descriptors import compute_descriptors
from src.controller.geometries_controller import GeometriesController
from src.object.shape import Shape
from src.pipeline.feature_extractor.shape_feature_extractor import ShapeFeatureExtractor
from src.database.writer import FeatureDatabaseWriter
from src.database.reader import FeatureDatabaseReader
from src.util.io import check_working_dir
from src.pipeline.normalization import Normalizer
from src.plot.feature_distribution import FeatureDistributionPlotter
from src.plot.confusion_matrix import ConfusionMatrixPlotter
from src.util.configs import *


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
    features_data = FeatureDatabaseReader.read_features(path)

    for shape in shape_list:
        if shape.geometries.path in features_data:
            shape.features = features_data[shape.geometries.path]


def add_shape_descriptors(shape_list: [Shape], path: str) -> None:
    descriptors_data = FeatureDatabaseReader.read_descriptors(path)

    for shape in shape_list:
        if shape.geometries.path in descriptors_data:
            shape.descriptors = descriptors_data[shape.geometries.path]


def add_shape_properties(shape_list: [Shape], path: str) -> None:
    properties_data = FeatureDatabaseReader.read_properties(path)

    for shape in shape_list:
        if shape.geometries.path in properties_data:
            shape.properties = properties_data[shape.geometries.path]


def save_state(shape_list: [Shape], recomputed_features: bool, recomputed_descriptors: bool, recomputed_properties: bool):
    if recomputed_features:
        FeatureDatabaseWriter.write_features(shape_list, os.path.join(DATABASE_NORMALIZED_DIR, DATABASE_FEATURES_FILENAME))
        FeatureDistributionPlotter.plot_features(PLOT_REFINED_FEATURES_DIR, [shape.features for shape in shape_list])

    if recomputed_descriptors or True:
        FeatureDatabaseWriter.write_descriptors(shape_list, os.path.join(DATABASE_NORMALIZED_DIR, DATABASE_DESCRIPTORS_FILENAME))
        normalized_shape_list = normalize_descriptors(os.path.join(DATABASE_NORMALIZED_DIR, DATABASE_DESCRIPTORS_FILENAME))

        # # Add properties to compute scalar and histogram features
        # for index in range(len(normalized_shape_list)):
        #     normalized_shape_list[index].properties = shape_list[index].properties
        #
        # # Recompute distance matrix on normalized descriptors and save to file
        # distances = calc_distances(normalized_shape_list)
        # distances.save(os.path.join(DATABASE_DIR, DATABASE_DISTANCES_FILENAME))

        # Reduce dimension on t-sne on weighted vectors
        dimensionality_reduction(normalized_shape_list)

    if recomputed_properties:
        FeatureDatabaseWriter.write_properties(shape_list, os.path.join(DATABASE_NORMALIZED_DIR, DATABASE_PROPERTIES_FILENAME))
        normalize_properties(os.path.join(DATABASE_NORMALIZED_DIR, DATABASE_PROPERTIES_FILENAME))


def plot(shape_list: [Shape], recomputed_descriptors: bool, recomputed_properties: bool, recompute_plots: bool = False):
    # Replot descriptors
    if recomputed_descriptors or recompute_plots:
        DescriptorDistributionPlotter.plot_descriptors(PLOT_REFINED_DESCRIPTORS_DIR, [shape.descriptors for shape in shape_list])
        normalized_descriptors = FeatureDatabaseReader.read_descriptors(os.path.join(DATABASE_NORMALIZED_DIR, DATABASE_NORMALIZED_DESCRIPTORS_FILENAME))
        DescriptorDistributionPlotter.plot_descriptors(PLOT_NORMALIZED_DESCRIPTORS_DIR, list(normalized_descriptors.values()))

    # Distance matrix plots
    if recomputed_descriptors or recomputed_properties or recompute_plots or True:
        distances = Distances(os.path.join(DATABASE_DIR, DATABASE_DISTANCES_FILENAME))
        DistanceMatrixPlotter.plot_distances(distances)

    # Confusion matrix plots
    if recomputed_descriptors or recompute_plots:
        normalized_descriptors = FeatureDatabaseReader.read_descriptors(os.path.join(DATABASE_NORMALIZED_DIR, DATABASE_NORMALIZED_DESCRIPTORS_FILENAME))
        ConfusionMatrixPlotter.plot(normalized_descriptors)

    # t-SNE plotting
    if recomputed_descriptors or recompute_plots:
        plot_tsne()

    # Plot distributions
    if recomputed_properties or recompute_plots:
        plot_property(shape_list, 'd1', 'Distance to center')
        plot_property(shape_list, 'd2', 'Distance between two vertices')
        plot_property(shape_list, 'd3', 'Area of triangle')
        plot_property(shape_list, 'd4', 'Volume of tetrahedron')
        plot_property(shape_list, 'a3', 'Angle between 3 vertices')


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
        FeatureDatabaseWriter.write_features(shape_list, os.path.join(DATABASE_ORIGINAL_DIR, DATABASE_FEATURES_FILENAME))
    if any(recomputed_features) or recompute_plots:
        FeatureDistributionPlotter.plot_features(PLOT_ORIGINAL_FEATURES_DIR, [shape.features for shape in shape_list])
    if any(recomputed_descriptors):
        FeatureDatabaseWriter.write_descriptors(shape_list, os.path.join(DATABASE_ORIGINAL_DIR, DATABASE_DESCRIPTORS_FILENAME))

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
    add_shape_properties(shape_list, os.path.join(DATABASE_NORMALIZED_DIR, DATABASE_PROPERTIES_FILENAME))

    print('\nCompute features of normalized shapes:\n')
    recomputed_features = []
    recomputed_descriptors = []
    recomputed_properties = []

    # All other features can be computed afterwards
    for shape in tqdm(shape_list):
        recomputed_features.append(ShapeFeatureExtractor.extract_all_shape_features(shape))
        recomputed_descriptors.append(compute_descriptors(shape))
        recomputed_properties.append(ShapePropertyExtractor.shape_propertizer(shape))

    recomputed_features = any(recomputed_features)
    recomputed_descriptors = any(recomputed_descriptors)
    recomputed_properties = any(recomputed_properties)

    save_state(shape_list, recomputed_features, recomputed_descriptors, recomputed_properties)
    plot(shape_list, recomputed_descriptors, recomputed_properties)


# Example loads an .off and .ply file
if __name__ == '__main__':
    logger.initialize()
    check_working_dir()
    matplotlib.use('agg')
    main()
    print("run complete")

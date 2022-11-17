"""
Entrypoint for the offline part of the application

For all shapes it goes through the steps one by one.
Results of the step are written to disk when all shapes are processed.
Results from a previous run get loaded in and their extraction will be skipped

The results of running this file are (Not exact in order):
1. Database file containing elementary features of unmodified shapes
2. Plots about the original normalization features
3. Normalized shapes
4. Plots of new normalization related features (To compare with step 2)
5. Database with features, descriptors, normalized descriptors, and properties
6. Matrix with distances for each part of the feature vector
7. Matrix with t-SNE coordinates
8. Plots for distances of each property
9. Plots for distances using a weighted vector
10. Plot for t-SNE with weighted vector
11. Plot for confusion matrix using a weighted vector
12. Plot for distributions of each property per class
"""

import os
from tqdm import tqdm
import sys
import matplotlib

# For VSCode: fix ModuleNotFoundError when importing.
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
    """Reads the original form of the shape,

    :return: List of shapes from the database
    """
    shape_list = []

    # Walk through labeledDB directory
    for sub_item in os.scandir(os.path.join("data", "LabeledDB_new")):
        if not sub_item.is_dir():
            continue

        for item in os.scandir(sub_item.path):
            if item.is_dir():
                continue

            # Database only contains *.off, so only load these
            if not item.path.endswith('.off'):
                continue

            # Database depends on relative paths
            shape = Shape(os.path.relpath(item.path))
            shape_list.append(shape)

    # Populates shape object with the features and descriptors
    add_shape_features(shape_list, os.path.join(DATABASE_ORIGINAL_DIR, DATABASE_FEATURES_FILENAME))
    add_shape_descriptors(shape_list, os.path.join(DATABASE_ORIGINAL_DIR, DATABASE_DESCRIPTORS_FILENAME))

    # Return list of shape objects
    return shape_list


def add_shape_features(shape_list: [Shape], path: str) -> None:
    """Adds the features to the shape from the database

    :param shape_list: List of shapes to load in features for
    :param path: Path to the database
    """
    # Read database
    features_data = FeatureDatabaseReader.read_features(path)

    # Loop through all the shapes
    for shape in shape_list:
        # Populate features by entry in the database if found
        if shape.geometries.path in features_data:
            shape.features = features_data[shape.geometries.path]


def add_shape_descriptors(shape_list: [Shape], path: str) -> None:
    """Adds the descriptors to the shape from a descriptor database

    :param shape_list: List of shapes to populate with descriptors
    :param path: Path to the descriptor database to load
    """
    # Read database
    descriptors_data = FeatureDatabaseReader.read_descriptors(path)

    # Loop through all shapes
    for shape in shape_list:
        # Populate descriptor if present in the database
        if shape.geometries.path in descriptors_data:
            shape.descriptors = descriptors_data[shape.geometries.path]


def add_shape_properties(shape_list: [Shape], path: str) -> None:
    """Adds the shape properties from the database if the file is present

    :param shape_list: List of shapes to load the properties of
    :param path: Path to the database which contains the properties (histgram bins)
    """
    # Load the properties data
    properties_data = FeatureDatabaseReader.read_properties(path)

    # Loop through each of the shapes
    for shape in shape_list:
        # Populate the properties if the path to the shape is present in database
        if shape.geometries.path in properties_data:
            shape.properties = properties_data[shape.geometries.path]


def process_database(recompute_plots: bool) -> ([Shape], bool, bool, bool):
    """Performs feature extraction, normalization and creates a few plots where needed
    Also, writes intermediate results of features, descriptors

    :param recompute_plots: Whether it should recompute plots
    :return: List of shapes, and which part of the data has been recomputed
    """
    # Compute offline features
    shape_list = read_original_shapes()

    # Compute the features and descriptors
    print('\nCompute features of original shapes:\n')
    recomputed_features = []
    recomputed_descriptors = []

    # Extract all features and compute descriptors if missing for all shapes
    for shape in tqdm(shape_list):
        recomputed_features.append(ShapeFeatureExtractor.extract_all_shape_features(shape))
        recomputed_descriptors.append(compute_descriptors(shape))

    # Only write file if new features are computed
    if any(recomputed_features):
        FeatureDatabaseWriter.write_features(shape_list, os.path.join(DATABASE_ORIGINAL_DIR, DATABASE_FEATURES_FILENAME))
    if any(recomputed_descriptors):
        FeatureDatabaseWriter.write_descriptors(shape_list, os.path.join(DATABASE_ORIGINAL_DIR, DATABASE_DESCRIPTORS_FILENAME))

    # Plot the elementary features
    if any(recomputed_features) or recompute_plots:
        FeatureDistributionPlotter.plot_features(PLOT_ORIGINAL_FEATURES_DIR, [shape.features for shape in shape_list])

    # Normalize shapes based on their point cloud representation
    print('\n--------------\nResample shapes + normalize')
    for shape in tqdm(shape_list):
        if not shape.geometries.path.endswith(FILENAME_ORIGINAL):
            continue

        # The database directory
        dir_path = os.path.split(shape.geometries.path)[0]
        poisson_pcd_path = os.path.join(dir_path, FILENAME_NORMALIZED_PCD)
        normalized_path = os.path.join(dir_path, FILENAME_NORMALIZED_PLY)

        # The shape had already been normalized, no need to recompute and normalize again
        if os.path.exists(poisson_pcd_path) and os.path.exists(normalized_path):
            shape.set_new_ply_path(normalized_path)
            continue

        # Make sure mesh and create uniform point cloud since PCA needs it
        GeometriesController.set_mesh_from_file(shape.geometries)
        shape.geometries.point_cloud = shape.geometries.mesh.sample_points_poisson_disk(NR_VERTICES, seed=0)

        # When normalization is performed, save the point cloud and ply version
        if Normalizer.normalize_shape(shape):
            shape.save_pcd(poisson_pcd_path)
            shape.save_ply(normalized_path)

        # This resets the previously computed convex hull
        shape.set_new_ply_path(normalized_path)

    # Load in shape features, descriptors, and properties for the normalized shapes
    add_shape_features(shape_list, os.path.join(DATABASE_NORMALIZED_DIR, DATABASE_FEATURES_FILENAME))
    add_shape_descriptors(shape_list, os.path.join(DATABASE_NORMALIZED_DIR, DATABASE_DESCRIPTORS_FILENAME))
    add_shape_properties(shape_list, os.path.join(DATABASE_NORMALIZED_DIR, DATABASE_PROPERTIES_FILENAME))

    # Compute features, descriptors, and properties that are still missing after loading them in
    print('\nCompute features of normalized shapes:\n')
    recomputed_features = []
    recomputed_descriptors = []
    recomputed_properties = []

    # For each shape initialize computing the different parts
    # If one of the things had a missing value, so is updated, then it will append True to the list
    # Using this method we know when the database or plots need to get updated
    for shape in tqdm(shape_list):
        recomputed_features.append(ShapeFeatureExtractor.extract_all_shape_features(shape))
        recomputed_descriptors.append(compute_descriptors(shape))
        recomputed_properties.append(ShapePropertyExtractor.shape_propertizer(shape))

    # If any of the features or alike have been recomputed any
    recomputed_features = any(recomputed_features)
    recomputed_descriptors = any(recomputed_descriptors)
    recomputed_properties = any(recomputed_properties)

    return shape_list, recomputed_features, recomputed_descriptors, recomputed_properties


def save_state(shape_list: [Shape], recomputed_features: bool, recomputed_descriptors: bool, recomputed_properties: bool) -> None:
    """Saves the state (computed features, descriptors, and properties) to files in the database

    :param shape_list: List of shapes containing the information for the database
    :param recomputed_features: Whether any features have been updated/computed
    :param recomputed_descriptors: Whether any descriptors have been updated/computed
    :param recomputed_properties: Whether any properties have been updated/computed
    """
    # Write the features to the database
    if recomputed_features:
        FeatureDatabaseWriter.write_features(shape_list, os.path.join(DATABASE_NORMALIZED_DIR, DATABASE_FEATURES_FILENAME))

    # Save recomputed descriptors to database and recompute
    if recomputed_descriptors:
        FeatureDatabaseWriter.write_descriptors(shape_list, os.path.join(DATABASE_NORMALIZED_DIR, DATABASE_DESCRIPTORS_FILENAME))
        normalized_shape_list = normalize_descriptors(os.path.join(DATABASE_NORMALIZED_DIR, DATABASE_DESCRIPTORS_FILENAME))

        # Add properties to compute scalar and histogram features
        for index in range(len(normalized_shape_list)):
            normalized_shape_list[index].properties = shape_list[index].properties

        # Recompute distance matrix on normalized descriptors and save to file
        distances = calc_distances(normalized_shape_list)
        distances.save(os.path.join(DATABASE_DIR, DATABASE_DISTANCES_FILENAME))

        # Reduce dimension on t-sne on weighted vectors
        dimensionality_reduction(normalized_shape_list)

    # If any properties got recomputed then write them to database and normalize it
    if recomputed_properties:
        FeatureDatabaseWriter.write_properties(shape_list, os.path.join(DATABASE_NORMALIZED_DIR, DATABASE_PROPERTIES_FILENAME))
        normalize_properties(os.path.join(DATABASE_NORMALIZED_DIR, DATABASE_PROPERTIES_FILENAME))


def plot(shape_list: [Shape], recomputed_features: bool, recomputed_descriptors: bool, recomputed_properties: bool, recompute_plots: bool = False) -> None:
    """Create the plots of different aspects of the shape, only if they have been updated

    :param shape_list: List of shapes containing the information to plot
    :param recomputed_features: Whether any features have been updated/computed
    :param recomputed_descriptors: Whether any descriptors have been updated/computed
    :param recomputed_properties: Whether any properties have been updated/computed
    :param recompute_plots: Override boolean to recompute plots even if no value got updated
    """
    if recomputed_features or recompute_plots:
        FeatureDistributionPlotter.plot_features(PLOT_REFINED_FEATURES_DIR, [shape.features for shape in shape_list])

    # Replot descriptors
    if recomputed_descriptors or recompute_plots:
        DescriptorDistributionPlotter.plot_descriptors(PLOT_REFINED_DESCRIPTORS_DIR, [shape.descriptors for shape in shape_list])
        normalized_descriptors = FeatureDatabaseReader.read_descriptors(os.path.join(DATABASE_NORMALIZED_DIR, DATABASE_NORMALIZED_DESCRIPTORS_FILENAME))
        DescriptorDistributionPlotter.plot_descriptors(PLOT_NORMALIZED_DESCRIPTORS_DIR, list(normalized_descriptors.values()))

    # Distance + confusion matrix plots
    if recomputed_descriptors or recomputed_properties or recompute_plots or True:
        distances = Distances(os.path.join(DATABASE_DIR, DATABASE_DISTANCES_FILENAME))
        DistanceMatrixPlotter.plot_distances(distances)

        # Calculate confusion matrices for different values of k
        ConfusionMatrixPlotter.plot(distances, k=5)
        ConfusionMatrixPlotter.plot(distances, k=10)
        ConfusionMatrixPlotter.plot(distances, k=20)

    # t-SNE plot
    if recomputed_descriptors or recompute_plots:
        plot_tsne()

    # Plot distributions for each shape category in histograms
    if recomputed_properties or recompute_plots:
        plot_property(shape_list, 'd1', 'Distance to center')
        plot_property(shape_list, 'd1', 'Distance to center')
        plot_property(shape_list, 'd2', 'Distance between two vertices')
        plot_property(shape_list, 'd3', 'Area of triangle')
        plot_property(shape_list, 'd4', 'Volume of tetrahedron')
        plot_property(shape_list, 'a3', 'Angle between 3 vertices')


def main() -> None:
    """Main function of the offline database processing"""
    # Initialize logger, check that the working directory is correctly set
    logger.initialize()
    check_working_dir()
    matplotlib.use('agg')

    # Hardcoded recompute plots
    recompute_plots = False

    # Processes database, saves certain things to database, and plots.
    shape_list, recomputed_features, recomputed_descriptors, recomputed_properties = process_database(recompute_plots)
    save_state(shape_list, recomputed_features, recomputed_descriptors, recomputed_properties)
    plot(shape_list, recomputed_features, recomputed_descriptors, recomputed_properties, recompute_plots)
    print("run complete")


# At the top of the file all the information is given
if __name__ == '__main__':
    main()

import os
from tqdm import tqdm

# Needed to fix ModuleNotFoundError when importing src.util.logger.
directoryContainingCurrentFile = os.path.dirname(__file__)
repoDirectory = os.path.dirname(directoryContainingCurrentFile)

# Add repo to list of possible paths
import sys
sys.path.append(repoDirectory)

from src.object.features.shape_features import ShapeFeatures
from src.pipeline.compute_descriptors import compute_descriptors
from src.pipeline.feature_extractor.mesh_feature_extractor import MeshFeatureExtractor
from src.pipeline.remeshing import Remesher
from src.plot.triangle_area import TriangleAreaPlotter
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
from src.vertex_normalization import refine_mesh


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


def remesh_and_save_shape(shape: Shape) -> None:
    GeometriesController.calculate_mesh(shape.geometries)

    Remesher.remesh_shape(shape)
    new_path = os.path.join(os.path.split(shape.geometries.path)[0], 'remeshed.ply')
    shape.geometries.path = new_path
    shape.save(shape.geometries.path)


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


def plot_feature_data(shape_collection: [Shape]) -> None:
    shape_features = [shape.features for shape in shape_collection]
    FeatureDistributionPlotter.plot_features(shape_features)


def refine_meshes(shape_collection: [Shape]) -> None:
    desired_number_of_vertices = 20000

    testShape = shape_collection[0]
    old_shape_path = testShape.geometries.path
    old_shape_vertices = testShape.features.mesh_features.nr_vertices

    #print(testShape)
    #print(old_shape_path)
    #print(old_shape_vertices)

    #refine_mesh(old_shape_path, old_shape_vertices, desired_number_of_vertices)

    print('========================= Refining meshes to desired number of vertices in the whole database ======================')

    finalVertexCounts = []

    for current_shape in shape_collection:
        current_shape_path = current_shape.geometries.path
        current_shape_vertices = current_shape.features.mesh_features.nr_vertices

        #print(f'item[{i}] = {pathToOriginalPLYMesh}')
        #print(originalVerticesOfPLYMesh)

        finalVertexCountOfThisMesh = refine_mesh(current_shape_path, current_shape_vertices, desired_number_of_vertices)
        finalVertexCounts.append(finalVertexCountOfThisMesh)

    # Create a histogram to show how well the algorithm performed.
    # hist_plot('Final vertex counts of refined meshed', finalVertexCounts)

    #print(f"Final vertex counts:\n{finalVertexCounts}")


def main():
    # Offline computed features
    shape_list = read_original_shapes()
    add_shape_features(shape_list, 'data/database/original_features.csv')
    add_shape_descriptors(shape_list, 'data/database/original_descriptors.csv')

    # Compute the features and descriptors
    # for shape in tqdm(shape_list):
    #     ShapeFeatureExtractor.extract_all_shape_features(shape)
    #     compute_descriptors(shape)
    #
    # DatabaseWriter.write_features(shape_list, 'data/database/original_features.csv')
    # DatabaseWriter.write_descriptors(shape_list, 'data/database/original_descriptors.csv')

    # print('Normalizing shapes')
    # How to then change the shape
    # for shape in shape_list:
    #     normalize_and_save_shape(shape)
    # shape_list = read_normalized_shapes()

    # Collect the paths to the Shapes too for refinement, if needed.
    # shapePaths = [shape.geometries.path for shape in shape_collection]

    plot_feature_data(shape_list)

    refine_meshes(shape_list)


# Example loads an .off and .ply file
if __name__ == '__main__':
    logger.initialize()
    check_working_dir()
    main()
    print("run complete")

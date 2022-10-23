import os
from tqdm import tqdm
import sys
import open3d as o3d
import shutil
import logging
import math

from matplotlib import pyplot as plt
import numpy as np

from src.database.querier import DatabaseQuerier
from src.object.descriptors import Descriptors
from src.pipeline.normalize_descriptors import normalize_descriptors, compute_normalized_descriptor

# Needed to fix ModuleNotFoundError when importing src.util.logger.
directoryContainingCurrentFile = os.path.dirname(__file__)
repoDirectory = os.path.dirname(directoryContainingCurrentFile)

# Add repo to list of possible paths
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
from src.vertex_normalization import refine_mesh, simplifyMesh, saveRefinedMesh


NR_VERTICES = 10000

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

    add_shape_features(shape_list, 'data/database/original_features.csv')
    add_shape_descriptors(shape_list, 'data/database/original_descriptors.csv')
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


def normalize_and_save_pcd(shape: Shape, new_path: str):
    if os.path.exists(new_path):
        return

    # When normalization is successful
    if Normalizer.normalize_shape(shape):
        shape.save_pcd(new_path)
        shape.geometries.path = new_path


def plot_feature_data(shape_collection: [Shape]) -> None:
    shape_features = [shape.features for shape in shape_collection]
    FeatureDistributionPlotter.plot_features(shape_features)


def refine_meshes(shape_collection: [Shape], final_vertices) -> None:
    testShape = shape_collection[140]
    old_shape_path = testShape.geometries.path

    #print(f'{old_shape_path}\n')

    #refine_mesh(old_shape_path, final_vertices)
    #prin()

    finalVertexCounts = []
    for current_shape in tqdm(shape_collection):
        current_shape_path = current_shape.geometries.path

        finalVertexCountOfThisMesh = refine_mesh(current_shape_path, final_vertices)
        finalVertexCounts.append(finalVertexCountOfThisMesh)

    # Create a histogram to check if the simplification performed well.
    final_counts = np.array(finalVertexCounts)

    #print(f'final_counts = {final_counts}')

    plt.hist(final_counts, bins = 100)
    plt.title('Final vertex counts of simplified meshes')

    plt.show()


def main():
    # Compute offline features
    shape_list = read_original_shapes()

    # Compute the features and descriptors
    print('\nCompute features of original shapes:\n')
    for shape in tqdm(shape_list):
        ShapeFeatureExtractor.extract_all_shape_features(shape)
        compute_descriptors(shape)

    DatabaseWriter.write_features(shape_list, 'data/database/original_features.csv')
    DatabaseWriter.write_descriptors(shape_list, 'data/database/original_descriptors.csv')

    normalize_descriptors('data/database/original_descriptors.csv')

    # querier = DatabaseQuerier('data/database/original_descriptors_normalized.csv')
    #
    # descriptor = Descriptors()
    # descriptor.surface_area = 0
    # descriptor.eccentricity = 0
    # descriptor.diameter = 1
    # descriptor.rectangularity = math.inf
    # descriptor.compactness = 2
    # compute_normalized_descriptor(descriptor)
    #
    # querier.query_normalized_descriptor(descriptor)

    # Remesh shapes
    print('\n--------------\nResample shapes + normalize')
    for shape in tqdm(shape_list):
        if not shape.geometries.path.endswith('original.ply'):
            continue

        new_path = os.path.join(os.path.split(shape.geometries.path)[0], 'normalized.pcd')

        # Path already exists, set path of shape to point cloud
        if os.path.exists(new_path):
            shape.geometries.path = new_path
            continue

        GeometriesController.set_mesh_from_file(shape.geometries)
        shape.geometries.point_cloud = shape.geometries.mesh.sample_points_poisson_disk(NR_VERTICES)
        normalize_and_save_pcd(shape, new_path)

    # Go from a normalized point cloud to a mesh
    print('\n--------------\nCreate normalized meshes')
    for shape in tqdm(shape_list):
        if not shape.geometries.path.endswith('normalized.pcd'):
            continue

        new_path = os.path.join(os.path.split(shape.geometries.path)[0], 'normalized.ply')
        if os.path.exists(new_path):
            shape.geometries.path = new_path
            shape.set_new_ply_path(new_path)
            continue

        point_cloud: o3d.geometry.PointCloud = o3d.io.read_point_cloud(shape.geometries.path)
        point_cloud.estimate_normals()
        point_cloud.orient_normals_consistent_tangent_plane(10)

        mesh, _ = o3d.geometry.TriangleMesh().create_from_point_cloud_poisson(point_cloud)
        mesh: o3d.geometry.TriangleMesh = mesh
        o3d.io.write_triangle_mesh(new_path, mesh)

        shape.set_new_ply_path(new_path)

    # Creating a mesh with 10k vertices from the normalized point cloud (with a poisson surface)
    print(f'\n--------------\nSimplifying normalized meshes to {NR_VERTICES} vertices')
    for shape in tqdm(shape_list):
        if not shape.geometries.path.endswith('normalized.ply'):
            continue

        new_path = os.path.join(os.path.split(shape.geometries.path)[0], 'refined.ply')
        if os.path.exists(new_path):
            shape.geometries.path = new_path
            shape.set_new_ply_path(new_path)
            continue

        refined_mesh, _ = simplifyMesh(shape.geometries.path, NR_VERTICES)
        refined_mesh.save_current_mesh(new_path)

        shape.set_new_ply_path(new_path)

    # plot_feature_data(shape_list)


# Example loads an .off and .ply file
if __name__ == '__main__':
    logger.initialize()
    check_working_dir()
    main()
    print("run complete")

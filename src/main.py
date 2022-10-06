import os

# Needed to fix ModuleNotFoundError when importing src.util.logger.
directoryContainingCurrentFile = os.path.dirname(__file__)
repoDirectory = os.path.dirname(directoryContainingCurrentFile)

# Add repo to list of possible paths
import sys
sys.path.append(repoDirectory)

import src.util.logger as logger
from src.object.shape import Shape
from src.pipeline.feature_extractor.shape_feature_extractor import ShapeFeatureExtractor
import src.util.plot
from src.database.writer import DatabaseWriter
from src.database.reader import DatabaseReader
from src.util.io import check_working_dir


def main():
    shape_collection = []
    # Offline computed features
    features_data = DatabaseReader.read_all_shape_features()

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
            rel_path = os.path.relpath(item.path)
            shape = Shape(rel_path)

            if shape.geometries.path in features_data:
                shape.features = features_data[shape.geometries.path]

            # Disable additional feature extraction, meshes are not watertight
            # ShapeFeatureExtractor.extract_axis_aligned_bounding_box(shape)
            # ShapeFeatureExtractor.extract_mesh_features(shape)
            # ShapeFeatureExtractor.extract_convex_hull_features(shape)
            # ShapeFeatureExtractor.extract_normalization_features(shape)
            # ShapeFeatureExtractor.extract_axis_aligned_bounding_box(shape)
            shape_collection.append(shape)

    # Collect the paths to the Shapes too for refinement, if needed.
    shapePaths = [shape.geometries.path for shape in shape_collection]

    # src.util.plot.plot_features([shape.features for shape in shape_collection], shapePaths)
    DatabaseWriter.write_all_shape_features(shape_collection)
    print("run complete")


# Example loads an .off and .ply file
if __name__ == '__main__':
    logger.initialize()
    check_working_dir()
    main()

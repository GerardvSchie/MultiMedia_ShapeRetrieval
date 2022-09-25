import logging
import os

# Needed to fix ModuleNotFoundError when importing src.util.logger.
directoryContainingCurrentFile = os.path.dirname(__file__)
repoDirectory = os.path.dirname(directoryContainingCurrentFile)

# Add repo to list of possible paths
import sys
sys.path.append(repoDirectory)

import src.util.logger as logger
from src.object.shape import Shape
from src.pipeline.feature_extractor import FeatureExtractor
import src.util.plot
import src.database.writer
import src.database.reader
from src.util.io import check_working_dir


def main():
    shape_collection = []
    # Offline computed features
    features_data = src.database.reader.read_from_file()

    # Walk through labeledDB directory
    for subdir, dirs, files in os.walk(os.path.join("data", "LabeledDB_new")):
        for file in files:
            if file.endswith(".off"):
                # Load shape and extract the features
                path = os.path.join(subdir, file)
                # Database depends on relative paths
                rel_path = os.path.relpath(path)
                feature_path = rel_path.replace(".off", ".ply")
                if features_data.__contains__(feature_path):
                    shape = Shape(path, features_data[feature_path])
                else:
                    shape = Shape(path)
                FeatureExtractor.extract_features(shape)

                shape_collection.append(shape)

    src.util.plot.plot_features([shape.features for shape in shape_collection])
    src.database.writer.write_to_file(shape_collection)

    #
    # off_example = Shape("data/example.off")
    # print(off_example.mesh)
    # ply_example = Shape("data/example.ply")
    # print(ply_example.mesh)
    #
    # FeatureExtractor.extract_features(ply_example)
    # print(ply_example.features.nr_vertices)
    # print(ply_example.features.nr_triangles)

    logging.info("jflsdjfsldk")


# Example loads an .off and .ply file
if __name__ == '__main__':
    logger.initialize()
    check_working_dir()
    main()

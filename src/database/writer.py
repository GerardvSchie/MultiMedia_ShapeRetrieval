import csv
import os
import numpy as np

from src.object.descriptors import Descriptors
from src.object.features.shape_features import ShapeFeatures
from src.object.shape import Shape
from src.object.properties import Properties


class FeatureDatabaseWriter:
    DESCRIPTORS_HEADER = ['path'] + Descriptors.NAMES
    FEATURES_HEADER = ['path'] + ShapeFeatures.NAMES
    PROPERTIES_HEADER = ['path'] + Properties.NAMES

    @staticmethod
    def write_features(shape_list: [Shape], path: str) -> None:
        """Write the features to a file in csv format

        :param shape_list: List of shapes of which to write the features
        :param path: Path to write the features to
        """
        os.makedirs(os.path.split(path)[0], exist_ok=True)

        with open(path, "w", newline='') as f:
            writer = csv.writer(f)

            # Write header to file
            writer.writerow(FeatureDatabaseWriter.FEATURES_HEADER)
            for shape in shape_list:
                writer.writerow(FeatureDatabaseWriter.get_features_list(shape))

    @staticmethod
    def write_descriptors(shape_list: [Shape], path: str) -> None:
        """Write the descriptors to a file in csv format

        :param shape_list: List of shapes of which to write the features
        :param path: Path to write the descriptors to
        """
        os.makedirs(os.path.split(path)[0], exist_ok=True)

        with open(path, "w", newline='') as f:
            writer = csv.writer(f)

            # Write header to file
            writer.writerow(FeatureDatabaseWriter.DESCRIPTORS_HEADER)
            for shape in shape_list:
                writer.writerow(FeatureDatabaseWriter.get_descriptors_list(shape))

    @staticmethod
    def write_properties(shape_list: [Shape], path: str):
        """Write the properties to a file in csv format

        :param shape_list: List of shapes of which to write the features
        :param path: Path to write the properties to
        """
        os.makedirs(os.path.split(path)[0], exist_ok=True)

        with open(path, "w", newline='') as f:
            writer = csv.writer(f)

            # Write header to file
            writer.writerow(FeatureDatabaseWriter.PROPERTIES_HEADER)
            for shape in shape_list:
                writer.writerow(FeatureDatabaseWriter.get_properties_list(shape))

    @staticmethod
    def get_features_list(shape: Shape) -> [object]:
        """Gets list of features with path as first item

        :param shape: Shape to get the features from
        :return: List with features and path
        """
        return [path_to_array(shape.geometries.path)] + shape.features.to_list()

    @staticmethod
    def get_descriptors_list(shape: Shape) -> [object]:
        """Gets list of descriptors with path as first item

        :param shape: Shape to get the descriptors from
        :return: List with descriptors and path
        """
        return [path_to_array(shape.geometries.path)] + shape.descriptors.to_list()

    @staticmethod
    def get_properties_list(shape: Shape) -> [object]:
        """Gets list of properties with path as first item

        :param shape: Shape to get the properties from
        :return: List with features and path
        """
        arr = [str(prop).replace('\n', '') for prop in shape.properties.to_list()]
        return [str(path_to_array(shape.geometries.path))] + arr


def path_to_array(path: str) -> np.array:
    """Separate a path into a list so separator does not matter

    :param path: Path to convert
    :return: Array with each directory as an item and filename as last
    """
    identifier = []
    while len(path) > 0:
        path, tail = os.path.split(path)
        identifier.append(tail)

    # Revers and return
    identifier.reverse()
    return np.array(identifier)

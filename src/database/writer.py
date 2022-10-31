import csv
import os
import numpy as np

from src.object.descriptors import Descriptors
from src.object.features.shape_features import ShapeFeatures
from src.object.shape import Shape
from src.object.properties import Properties


class DatabaseWriter:
    DESCRIPTORS_HEADER = ['path'] + Descriptors.NAMES
    FEATURES_HEADER = ['path'] + ShapeFeatures.NAMES
    PROPERTIES_HEADER = ['path'] + Properties.NAMES

    @staticmethod
    def write_features(shape_list: [Shape], path: str):
        os.makedirs(os.path.split(path)[0], exist_ok=True)

        with open(path, "w", newline='') as f:
            writer = csv.writer(f)

            # Write header to file
            writer.writerow(DatabaseWriter.FEATURES_HEADER)
            for shape in shape_list:
                writer.writerow(DatabaseWriter.get_features_list(shape))

    @staticmethod
    def write_descriptors(shape_list: [Shape], path: str):
        os.makedirs(os.path.split(path)[0], exist_ok=True)

        with open(path, "w", newline='') as f:
            writer = csv.writer(f)

            # Write header to file
            writer.writerow(DatabaseWriter.DESCRIPTORS_HEADER)
            for shape in shape_list:
                writer.writerow(DatabaseWriter.get_descriptors_list(shape))

    @staticmethod
    def write_properties(shape_list: [Shape], path: str):
        os.makedirs(os.path.split(path)[0], exist_ok=True)

        with open(path, "w", newline='') as f:
            writer = csv.writer(f)

            # Write header to file
            writer.writerow(DatabaseWriter.PROPERTIES_HEADER)
            for shape in shape_list:
                writer.writerow(DatabaseWriter.get_properties_list(shape))

    @staticmethod
    def get_features_list(shape: Shape) -> [object]:
        return [path_to_array(shape.geometries.path)] + shape.features.to_list()

    @staticmethod
    def get_descriptors_list(shape: Shape) -> [object]:
        return [path_to_array(shape.geometries.path)] + shape.descriptors.to_list()

    @staticmethod
    def get_properties_list(shape: Shape) -> [object]:
        return [path_to_array(shape.geometries.path)] + shape.properties.to_list()


def path_to_array(path: str):
    identifier = []
    while len(path) > 0:
        path, tail = os.path.split(path)
        identifier.append(tail)

    identifier.reverse()
    return np.array(identifier)

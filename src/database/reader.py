import csv
import logging
import os.path
import numpy as np

from src.object.descriptors import Descriptors
from src.object.features.shape_features import ShapeFeatures

dataPaths = list()


class DatabaseReader:
    @staticmethod
    def read_features(path: str) -> dict[str, ShapeFeatures]:
        shape_features = dict()
        if not os.path.exists(path):
            logging.warning(f'Features path: {path} does not exist')
            return shape_features

        with open(path, "r") as f:
            # Create reader and skip header
            reader = csv.reader(f)
            next(reader)

            for features in reader:
                data = ShapeFeatures()

                # Global features
                identifier = features[0]
                data.true_class = features[1]
                data.is_watertight = features[2].lower() == 'true'
                data.diameter = float(features[3])

                # Mesh features
                data.mesh_features.nr_vertices = int(features[4])
                data.mesh_features.nr_faces = int(features[5])
                data.mesh_features.surface_area = float(features[6])
                data.mesh_features.volume = float(features[7])

                # Convex hull features
                data.convex_hull_features.nr_vertices = int(features[8])
                data.convex_hull_features.nr_faces = int(features[9])
                data.convex_hull_features.surface_area = float(features[10])
                data.convex_hull_features.volume = float(features[11])

                # AABB features
                data.axis_aligned_bounding_box_features.min_bound = _read_np_array(features[12])
                data.axis_aligned_bounding_box_features.max_bound = _read_np_array(features[13])
                data.axis_aligned_bounding_box_features.surface_area = float(features[14])
                data.axis_aligned_bounding_box_features.volume = float(features[15])
                data.axis_aligned_bounding_box_features.diameter = float(features[16])

                # Normalization features
                data.normalization_features.distance_to_center = float(features[17])
                data.normalization_features.scale = float(features[18])
                data.normalization_features.alignment = float(features[19])
                data.normalization_features.flip = int(features[20])
                data.normalization_features.eigenvalues = _read_np_array(features[21])

                # Set path
                path = os.path.join(*(_read_np_array(identifier)))
                shape_features[path] = data

        return shape_features

    @staticmethod
    def read_descriptors(path: str) -> dict[str, Descriptors]:
        shape_descriptors = dict()
        if not os.path.exists(path):
            logging.warning(f'Descriptors path: {path} does not exist')
            return shape_descriptors

        with open(path, "r") as f:
            # Read csv file and skip header
            reader = csv.reader(f)
            next(reader)

            for descriptor in reader:
                data = Descriptors()

                # Descriptors
                identifier = descriptor[0]
                data.surface_area = float(descriptor[1])
                data.compactness = float(descriptor[2])
                data.rectangularity = float(descriptor[3])
                data.diameter = float(descriptor[4])
                data.eccentricity = float(descriptor[5])

                # Set path
                path = os.path.join(*(_read_np_array(identifier)))
                shape_descriptors[path] = data

        return shape_descriptors


def _read_np_array(array_str: str) -> np.array:
    # Contains strings
    if array_str.__contains__("'"):
        arr = array_str[2:-2].split("\' \'")
        return np.array(arr)
    # Just an int array
    else:
        array_str = array_str.strip()
        arr = array_str[1:-1].strip().split()
        return np.array(arr, dtype=float)

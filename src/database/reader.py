import csv
import logging
import os.path

from src.object.descriptors import Descriptors
from src.object.features.shape_features import ShapeFeatures
from src.object.properties import Properties
from src.database.util import read_np_array

dataPaths = list()


class FeatureDatabaseReader:
    @staticmethod
    def read_features_paths(paths: [str]) -> dict[str, ShapeFeatures]:
        """Reads all features from the dictionary

        :param paths: List of paths to read
        :return: Dictionary containing features for each path
        """
        shape_features = dict()

        # Union features dictionaries together
        for path in paths:
            shape_features = shape_features | FeatureDatabaseReader.read_features(path)

        # Return dictionary with all shape features
        return shape_features

    @staticmethod
    def read_features(path: str) -> dict[str, ShapeFeatures]:
        """Read the features from the given path, it reads from a csv file

        :param path: Database path to read features from
        :return: Shape features in a dictionary
        """
        # If database path does not exist, return empty dictionary
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
                data.from_list(features[1:])

                # Reconstruct path
                path = os.path.join(*(read_np_array(identifier)))
                shape_features[path] = data

        # Dictionary with shape features
        return shape_features

    @staticmethod
    def read_descriptors(path: str) -> dict[str, Descriptors]:
        """Read the descriptors from the given path, it reads from a csv file

        :param path: Database path to read descriptors from
        :return: Shape descriptors in a dictionary
        """
        # If database path does not exist, return empty dictionary
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
                identifier = descriptor[0]
                data.from_list(descriptor[1:])

                # Set path
                path = os.path.join(*(read_np_array(identifier)))
                shape_descriptors[path] = data

        return shape_descriptors

    @staticmethod
    def read_properties(path: str) -> dict[str, Properties]:
        """Read the properties from the given path, it reads from a csv file

        :param path: Database path to read properties from
        :return: Shape properties in a dictionary
        """
        # If database path does not exist, return empty dictionary
        shape_properties = dict()
        if not os.path.exists(path):
            logging.warning(f'Properties path: {path} does not exist')
            return shape_properties

        with open(path, "r") as f:
            # Read csv file and skip header
            reader = csv.reader(f)
            next(reader)

            for properties in reader:
                data = Properties()
                identifier = properties[0]
                data.from_list(properties[1:])

                # Set path
                path = os.path.join(*(read_np_array(identifier)))
                shape_properties[path] = data

        # Return dictionary with properties
        return shape_properties

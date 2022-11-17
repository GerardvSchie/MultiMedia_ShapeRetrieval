import logging

from src.object.shape import Shape
from src.database.reader import FeatureDatabaseReader
from src.util.configs import *


def check_working_dir() -> None:
    """Sanity check to verify script is ran from the correct directory"""
    # Checks for both src and app folder in current directory
    src_exists = os.path.exists("src")
    app_exists = os.path.exists("app")

    # Raise exception if the script is not ran from the correct directory
    if not src_exists or not app_exists:
        logging.critical("Script is ran from the wrong directory\n"
                         "Could not find ./src or ./app directory.\n"
                         "Please run the script from the repository root using\n"
                         "python src/main.py\n"
                         "or\n"
                         "python app/main.py")
        raise Exception("Critical error. Please read logfile or console for more information")


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

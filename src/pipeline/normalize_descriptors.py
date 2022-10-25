import numpy as np
import os
from configparser import ConfigParser

from src.database.reader import DatabaseReader
from src.database.writer import DatabaseWriter
from src.object.descriptors import Descriptors
from src.object.shape import Shape
from src.util.configs import *


def normalize_descriptors(path: str) -> None:
    descriptors = DatabaseReader.read_descriptors(path)
    dir_name, filename = os.path.split(path)

    # Initialize lists
    identifiers = []
    surface_area = []
    compactness = []
    rectangularity = []
    diameter = []
    eccentricity = []

    # Fill lists with data
    for identifier in descriptors:
        descriptor = descriptors[identifier]

        identifiers.append(identifier)
        surface_area.append(descriptor.surface_area)
        compactness.append(descriptor.compactness)
        rectangularity.append(descriptor.rectangularity)
        diameter.append(descriptor.diameter)
        eccentricity.append(descriptor.eccentricity)

    # Normalize descriptors
    config = ConfigParser()

    surface_area = _normalize_descriptor(surface_area, config, 'surface_area')
    compactness = _normalize_descriptor(compactness, config, 'compactness')
    rectangularity = _normalize_descriptor(rectangularity, config, 'rectangularity')
    diameter = _normalize_descriptor(diameter, config, 'diameter')
    eccentricity = _normalize_descriptor(eccentricity, config, 'eccentricity')

    config_name = filename.split('.')[0] + '.ini'
    with open(os.path.join(dir_name, config_name), 'w') as configfile:
        config.write(configfile)

    shape_list = []
    # Replace data with normalized values
    for index in range(len(identifiers)):
        identifier = identifiers[index]
        descriptors[identifier].surface_area = surface_area[index]
        descriptors[identifier].compactness = compactness[index]
        descriptors[identifier].rectangularity = rectangularity[index]
        descriptors[identifier].diameter = diameter[index]
        descriptors[identifier].eccentricity = eccentricity[index]

        shape = Shape(identifier)
        shape.descriptors = descriptors[identifier]
        shape_list.append(shape)

    DatabaseWriter.write_descriptors(shape_list, os.path.join(dir_name, DATABASE_NORMALIZED_DESCRIPTORS_FILENAME))


def _normalize_descriptor(data: [float], config: ConfigParser, name: str):
    data = np.array(data)
    avg = np.average(data)
    std = np.std(data)

    config[name] = {
        'average': avg,
        'standard_deviation': std,
    }

    return (data - avg) / std


def compute_normalized_descriptor(descriptors: Descriptors):
    config = ConfigParser()
    config.read([os.path.join(DATABASE_REFINED_DIR, DATABASE_DESCRIPTORS_INI)])

    descriptors.surface_area = (descriptors.surface_area - float(config['surface_area']['average'])) / float(config['surface_area']['standard_deviation'])
    descriptors.compactness = (descriptors.compactness - float(config['compactness']['average'])) / float(config['compactness']['standard_deviation'])
    descriptors.rectangularity = (descriptors.rectangularity - float(config['rectangularity']['average'])) / float(config['rectangularity']['standard_deviation'])
    descriptors.diameter = (descriptors.diameter - float(config['diameter']['average'])) / float(config['diameter']['standard_deviation'])
    descriptors.eccentricity = (descriptors.eccentricity - float(config['eccentricity']['average'])) / float(config['eccentricity']['standard_deviation'])

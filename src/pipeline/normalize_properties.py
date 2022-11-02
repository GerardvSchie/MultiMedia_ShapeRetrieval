import numpy as np
import os
from configparser import ConfigParser

from src.database.reader import DatabaseReader
from src.database.writer import DatabaseWriter
from src.object.properties import Properties
from src.object.shape import Shape
from src.util.configs import *


def normalize_properties(path: str) -> None:
    properties_dict = DatabaseReader.read_properties(path)
    dir_name, filename = os.path.split(path)

    # Fill lists with data
    properties_array = np.ndarray(shape=(len(properties_dict), len(Properties.NAMES), Properties.NR_BINS), dtype=float)
    identifiers = []
    i = 0
    for identifier in properties_dict:
        identifiers.append(identifier)
        properties_array[i] = np.array(properties_dict[identifier].to_list())
        i += 1

    # Normalize descriptors
    config = ConfigParser()
    descriptors_array = np.transpose(properties_array, axes=(1, 2, 0))

    for i in range(len(Properties.NAMES)):
        descriptors_array[i] = _normalize_property(descriptors_array[i], config, Properties.NAMES[i])

    config_name = filename.split('.')[0] + '.ini'
    with open(os.path.join(dir_name, config_name), 'w') as configfile:
        config.write(configfile)

    shape_list = []
    descriptors_array = np.transpose(descriptors_array, axes=(2, 0, 1))
    # Replace data with normalized values
    for index in range(len(identifiers)):
        identifier = identifiers[index]
        properties_list = list(descriptors_array[index])
        properties_dict[identifier].from_list(properties_list)

        shape = Shape(identifier)
        shape.properties = properties_dict[identifier]
        shape_list.append(shape)

    DatabaseWriter.write_properties(shape_list, os.path.join(dir_name, DATABASE_NORMALIZED_PROPERTIES_FILENAME))


def _normalize_property(data: np.array, config: ConfigParser, name: str):
    avg = np.average(data, axis=1)
    std = np.std(data, axis=1)

    config[name] = {
        'average': avg,
        'standard_deviation': std,
    }

    avg_repeated = np.repeat(avg, 380).reshape(Properties.NR_BINS, 380)
    std_repeated = np.repeat(std, 380).reshape(Properties.NR_BINS, 380)

    return np.divide(data - avg_repeated, std_repeated, out=np.zeros_like(data), where=std_repeated != 0)

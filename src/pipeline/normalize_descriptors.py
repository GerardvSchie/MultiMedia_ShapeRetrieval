from configparser import ConfigParser

from database.features.reader import FeatureDatabaseReader
from database.features.writer import FeatureDatabaseWriter
from src.object.descriptors import Descriptors
from src.object.shape import Shape
from src.util.configs import *


def normalize_descriptors(path: str) -> None:
    descriptors_dict = FeatureDatabaseReader.read_descriptors(path)
    dir_name, filename = os.path.split(path)

    # Fill lists with data
    descriptors_array = np.ndarray(shape=(len(descriptors_dict), len(Descriptors.NAMES)), dtype=float)
    identifiers = []
    i = 0
    for identifier in descriptors_dict:
        identifiers.append(identifier)
        descriptors_array[i] = np.array(descriptors_dict[identifier].to_list())
        i += 1

    # Normalize descriptors (transpose so each feature is a row
    config = ConfigParser()
    descriptors_array = np.transpose(descriptors_array)

    for i in range(len(Descriptors.NAMES)):
        descriptors_array[i] = _normalize_descriptor(descriptors_array[i], config, Descriptors.NAMES[i])

    config_name = filename.split('.')[0] + '.ini'
    with open(os.path.join(dir_name, config_name), 'w') as configfile:
        config.write(configfile)

    shape_list = []
    descriptors_array = np.transpose(descriptors_array)
    # Replace data with normalized values
    for index in range(len(identifiers)):
        identifier = identifiers[index]
        descriptors_list = list(descriptors_array[index])
        descriptors_dict[identifier].from_list(descriptors_list)

        shape = Shape(identifier)
        shape.descriptors = descriptors_dict[identifier]
        shape_list.append(shape)

    FeatureDatabaseWriter.write_descriptors(shape_list, os.path.join(dir_name, DATABASE_NORMALIZED_DESCRIPTORS_FILENAME))


def _normalize_descriptor(data: np.array, config: ConfigParser, name: str):
    avg = np.average(data)
    std = np.std(data)

    config[name] = {
        'average': avg,
        'standard_deviation': std,
    }

    return (data - avg) / std


def compute_normalized_descriptor(descriptors: Descriptors):
    config = ConfigParser()
    config.read([os.path.join(DATABASE_NORMALIZED_DIR, DATABASE_DESCRIPTORS_INI)])

    for attribute in Descriptors.NAMES:
        val = descriptors.__getattribute__(attribute)
        new_val = (val - float(config[attribute]['average'])) / float(config[attribute]['standard_deviation'])
        descriptors.__setattr__(attribute, new_val)

from configparser import ConfigParser

from src.database.reader import FeatureDatabaseReader
from src.database.writer import FeatureDatabaseWriter
from src.object.descriptors import Descriptors
from src.object.shape import Shape
from src.util.configs import *


def normalize_descriptors(path: str) -> [Shape]:
    """Creates a list of shapes with the normalized descriptor values

    :param path: Path of the file containing the descriptors
    :return: List of shapes of which the descriptors have been normalized
    """
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

    # Normalize descriptors (transpose so each feature is a row)
    config = ConfigParser()
    descriptors_array = np.transpose(descriptors_array)

    # Normalize each descriptor
    for i in range(len(Descriptors.NAMES)):
        descriptors_array[i] = _normalize_descriptor(descriptors_array[i], config, Descriptors.NAMES[i])

    # Write the averages and standard deviations to .ini file
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

    # Writes the descriptors to file
    FeatureDatabaseWriter.write_descriptors(shape_list, os.path.join(dir_name, DATABASE_NORMALIZED_DESCRIPTORS_FILENAME))
    return shape_list


def _normalize_descriptor(data: np.array, config: ConfigParser, name: str) -> np.array:
    """Normalizes the data containing the descriptors

    :param data: Data to normalize
    :param config: Save the mean and standard deviation to config to later write to file
    :param name: Name of the property to normalize
    :return: Normalized descriptors matrix
    """
    avg = np.average(data)
    std = np.std(data)

    # Save the average
    config[name] = {
        'average': avg,
        'standard_deviation': std,
    }

    # Normalized data
    return (data - avg) / std


def compute_normalized_descriptor(descriptors: Descriptors):
    """Normalizes a single descriptor

    :param descriptors: Descriptor to normalize
    :return: Normalized descriptors
    """
    config = ConfigParser()
    config.read([os.path.join(DATABASE_NORMALIZED_DIR, DATABASE_DESCRIPTORS_INI)])

    # Normalizes each attribute
    for attribute in Descriptors.NAMES:
        val = descriptors.__getattribute__(attribute)
        new_val = (val - float(config[attribute]['average'])) / float(config[attribute]['standard_deviation'])
        descriptors.__setattr__(attribute, new_val)

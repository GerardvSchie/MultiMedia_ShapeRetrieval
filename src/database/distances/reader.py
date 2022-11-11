from configparser import ConfigParser

from database.features.reader import FeatureDatabaseReader
from database.features.writer import FeatureDatabaseWriter
from src.object.properties import Properties
from src.object.shape import Shape
from src.util.configs import *


class DistancesDatabaseReader:
    @staticmethod
    def read_distances(database_path):
        config = ConfigParser()
        config.read([os.path.join(DATABASE_NORMALIZED_DIR, DATABASE_DESCRIPTORS_INI)])

        for attribute in Descriptors.NAMES:
            val = descriptors.__getattribute__(attribute)
            new_val = (val - float(config[attribute]['average'])) / float(config[attribute]['standard_deviation'])
            descriptors.__setattr__(attribute, new_val)

import numpy as np
import math

from src.object.descriptors import Descriptors
from src.object.shape import Shape


def compute_descriptors(shape: Shape):
    if not shape.descriptors.missing_values():
        return

    descriptors: Descriptors = Descriptors()

    descriptors.surface_area = shape.features.mesh_features.surface_area
    descriptors.compactness = np.power(shape.features.mesh_features.surface_area, 3) / (36 * math.pi * np.power(shape.features.mesh_features.volume, 2))
    descriptors.rectangularity = shape.features.mesh_features.volume / shape.features.axis_aligned_bounding_box_features.volume
    descriptors.diameter = shape.features.diameter
    descriptors.eccentricity = shape.features.normalization_features.eigenvalues[0] / shape.features.normalization_features.eigenvalues[2]

    shape.descriptors = descriptors

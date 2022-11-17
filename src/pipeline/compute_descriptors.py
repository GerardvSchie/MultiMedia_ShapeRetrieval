import numpy as np
import math

from src.object.descriptors import Descriptors
from src.object.shape import Shape


def compute_descriptors(shape: Shape) -> bool:
    """Computes descriptors of the given shape

    :param shape: Shape to compute descriptors of
    :return: Whether new descriptor values were computed
    """
    if not shape.descriptors.missing_values():
        return False

    # Descriptor object to save to
    descriptors: Descriptors = Descriptors()

    descriptors.surface_area = shape.features.mesh_features.surface_area
    descriptors.compactness = np.power(shape.features.mesh_features.surface_area, 3) / (36 * math.pi * np.power(shape.features.mesh_features.volume, 2))
    descriptors.sphericity = 1 / descriptors.compactness
    descriptors.rectangularity = shape.features.mesh_features.volume / shape.features.axis_aligned_bounding_box_features.volume
    descriptors.convexity = shape.features.mesh_features.volume / shape.features.convex_hull_features.volume
    descriptors.diameter = shape.features.diameter

    # Eccentricity descriptors
    descriptors.eccentricity = shape.features.normalization_features.eigenvalues[0] / shape.features.normalization_features.eigenvalues[2]
    descriptors.major_eccentricity = shape.features.normalization_features.eigenvalues[0] / shape.features.normalization_features.eigenvalues[1]
    descriptors.minor_eccentricity = shape.features.normalization_features.eigenvalues[1] / shape.features.normalization_features.eigenvalues[2]

    # Assign descriptors to shape and indicate a descriptor got computed
    shape.descriptors = descriptors
    return True

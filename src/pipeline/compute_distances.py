from object.distances import Distances
from src.object.shape import Shape
from src.object.descriptors import Descriptors
from src.util.configs import *


def calc_distances(shape_list: [Shape]) -> Distances():
    vectors = np.array([shape.descriptors.to_list() for shape in shape_list])
    distances = Distances()

    distance_matrix: np.ndarray = np.zeros(shape=(len(vectors), len(vectors), len(Descriptors.NAMES)))
    for index in range(len(vectors)):
        vecs = vectors - vectors[index]
        distance_matrix[index] = vecs

    distances.matrix = np.transpose(distance_matrix, (2, 0, 1))
    return distances

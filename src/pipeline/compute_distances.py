from pyemd import emd
from tqdm import tqdm
from scipy.stats import entropy
from scipy.spatial.distance import jensenshannon

from src.object.properties import Properties
from src.object.distances import Distances
from src.object.shape import Shape
from src.object.descriptors import Descriptors
from src.util.configs import *


def calc_distances(shape_list: [Shape]) -> Distances:
    distances = Distances()

    # Handle descriptors
    descriptor_vectors = np.array([shape.descriptors.to_list() for shape in shape_list])
    calc_descriptor_distances(descriptor_vectors, distances)

    # Handle properties
    calc_property_distances(shape_list, distances)

    return distances


def calc_descriptor_distances(vectors: np.array, distances: Distances) -> None:
    distance_matrix: np.ndarray = np.zeros(shape=(NR_SHAPES, NR_SHAPES, len(Descriptors.NAMES)))
    for index in range(NR_SHAPES):
        relative_vectors = vectors - vectors[index]
        distance_matrix[index] = relative_vectors

    transposed_distance_matrices = np.transpose(distance_matrix, (2, 0, 1))
    for i in range(len(Descriptors.NAMES)):
        distances.matrix[i] = transposed_distance_matrices[i]


def calc_property_distances(shape_list: [Shape], distances: Distances) -> None:
    distance_matrix: np.ndarray = np.zeros(shape=(len(Properties.NAMES), NR_SHAPES, NR_SHAPES))

    j = 0
    for property_name in Properties.NAMES:
        distance_matrix[j] = calc_emd_distance_matrix(shape_list, property_name)
        j += 1

    for j in range(len(Properties.NAMES)):
        distances.matrix[len(Descriptors.NAMES) + j] = distance_matrix[j]


def calc_emd_distance_matrix(shape_list: [Shape], attribute: str) -> np.ndarray:
    n = Properties.NR_BINS
    # Uniform
    # distance_matrix = np.full((n, n), 1.0)

    # DIAGONAL
    arr = np.arange(0.0, 1.0, 1.0 / n)
    meshgrid = np.array(np.meshgrid(arr, arr)).T.reshape(-1, 2)
    diff = meshgrid[:, 0] - meshgrid[:, 1]
    abs_diff = np.abs(diff)
    power_abs_diff = np.power(abs_diff, 2)
    distance_matrix = power_abs_diff.reshape(n, n)

    # Threshold
    # arr = np.arange(0.0, 1.0, 1.0 / n)
    # meshgrid = np.array(np.meshgrid(arr, arr)).T.reshape(-1, 2)
    # diff = meshgrid[:, 0] - meshgrid[:, 1]
    # abs_diff = np.abs(diff)
    # distance_matrix = (abs_diff > 0.1) * 1.0
    # distance_matrix = distance_matrix.reshape(n, n)

    # Threshold + Diagonal
    # arr = np.arange(0.0, 1.0, 1.0 / n)
    # meshgrid = np.array(np.meshgrid(arr, arr)).T.reshape(-1, 2)
    # diff = meshgrid[:, 0] - meshgrid[:, 1]
    # abs_diff = np.abs(diff)
    # abs_diff[abs_diff < 0.2] = 0.0
    # distance_matrix = abs_diff.reshape(n, n)

    result_matrix = np.full((NR_SHAPES, NR_SHAPES), 0.0)
    # result_matrix = np.zeros((NR_SHAPES, NR_SHAPES), dtype=float)
    i = 0
    for shape_1 in tqdm(shape_list):
        j = 0
        arr1 = shape_1.properties.__getattribute__(attribute)
        for shape_2 in shape_list:
            val = emd(arr1, shape_2.properties.__getattribute__(attribute), distance_matrix)
            result_matrix[i, j] = val
            j += 1
        i += 1

    return result_matrix


def calc_entropy(shape_dict: dict[str, Shape], attribute: str) -> np.ndarray:
    result_matrix = np.full((len(shape_dict), len(shape_dict)), 0.0)
    i = 0
    for path_i in tqdm(shape_dict):
        j = 0
        arr1 = shape_dict[path_i].properties.__getattribute__(attribute) + 0.0001
        for path_j in shape_dict:
            arr2 = shape_dict[path_j].properties.__getattribute__(attribute) + 0.0001
            result_matrix[i, j] = (entropy(arr1, arr2) + entropy(arr2, arr1)) / 2
            j += 1
        i += 1

    return result_matrix


def calc_jensen_shannon(shape_dict: dict[str, Shape], attribute: str) -> np.ndarray:
    result_matrix = np.full((len(shape_dict), len(shape_dict)), 0.0)
    i = 0
    for path_i in tqdm(shape_dict):
        j = 0
        arr1 = shape_dict[path_i].properties.__getattribute__(attribute)
        for path_j in shape_dict:
            arr2 = shape_dict[path_j].properties.__getattribute__(attribute)
            result_matrix[i, j] = jensenshannon(arr1, arr2)
            j += 1
        i += 1

    return result_matrix


def calc_euclidian_distance(shape_dict: dict[str, Shape], attribute: str) -> np.ndarray:
    result_matrix = np.full((len(shape_dict), len(shape_dict)), 0.0)
    i = 0
    for path_i in tqdm(shape_dict):
        j = 0
        arr1 = shape_dict[path_i].properties.__getattribute__(attribute)
        for path_j in shape_dict:
            arr2 = shape_dict[path_j].properties.__getattribute__(attribute)

            # Absolute distance
            diff_arr = arr1 - arr2
            result_matrix[i, j] = np.sum(np.abs(diff_arr))

            # Euclidian
            # diff_arr = arr1 - arr2
            # squared_dif_arr = np.power(diff_arr, 2)
            # distance = np.sqrt(np.sum(squared_dif_arr))
            # result_matrix[i, j] = distance
            j += 1
        i += 1

    return result_matrix

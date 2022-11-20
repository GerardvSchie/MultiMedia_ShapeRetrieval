from pyemd import emd
from tqdm import tqdm
from scipy.stats import entropy
from scipy.spatial.distance import jensenshannon

from src.object.properties import Properties
from src.object.distances import Distances
from src.object.shape import Shape
from src.object.descriptors import Descriptors
from src.util.configs import *


def calc_distance_matrix_emd(shape_list: [Shape]) -> Distances:
    """Calculates the distance matrix using emd distance for histograms

    :param shape_list: List of shapes of which the distances are computed
    :return: The computed distances
    """
    distances = Distances()

    # Handle descriptors and property distances
    calc_descriptor_distances(shape_list, distances)
    calc_property_distances_emd(shape_list, distances)

    return distances


def calc_distance_matrix_knn(shape_list: [Shape]) -> Distances:
    """Calculates the distance matrix using euclidian distance for the entire vector
    This is for usage in KNN searching

    :param shape_list: List of shapes of which the distances are computed
    :return: The computed distances
    """
    distances = Distances()
    distances.matrix = np.full((len(Descriptors.NAMES) + len(Properties.NAMES) * 20, 380, 380), np.inf)

    # Handle descriptors and property distances
    calc_descriptor_distances(shape_list, distances)
    calc_property_distances_knn(shape_list, distances)

    return distances


def calc_descriptor_distances(shape_list: [Shape], distances: Distances) -> None:
    """Calculates the distances for each descriptor in an N x N matrix

    :param shape_list: List of shapes of which the distances are computed
    :param distances: Contains matrix with distances of each descriptor
    """
    vectors = np.array([shape.descriptors.to_list() for shape in shape_list])
    distance_matrix: np.ndarray = np.zeros(shape=(NR_SHAPES, NR_SHAPES, len(Descriptors.NAMES)))

    for index in range(NR_SHAPES):
        relative_vectors = vectors - vectors[index]
        distance_matrix[index] = relative_vectors

    # Each descriptor is a slice in the matrix
    transposed_distance_matrices = np.transpose(distance_matrix, (2, 0, 1))
    for i in range(len(Descriptors.NAMES)):
        distances.matrix[i] = transposed_distance_matrices[i]


def calc_property_distances_emd(shape_list: [Shape], distances: Distances) -> None:
    """Calculates the distances between the shapes

    :param shape_list: List of shapes of which the distances are computed
    :param distances: Contains matrix with distances of descriptors and properties to save to
    """
    distance_matrix: np.ndarray = np.zeros(shape=(len(Properties.NAMES), NR_SHAPES, NR_SHAPES))

    j = 0
    for property_name in Properties.NAMES:
        for index in range(NR_SHAPES):
            distance_matrix[j] = calc_emd_distance_matrix(shape_list, property_name)
        j += 1

    # Fill slice
    for j in range(len(Properties.NAMES)):
        distances.matrix[len(Descriptors.NAMES) + j] = distance_matrix[j]


def calc_property_distances_knn(shape_list: [Shape], distances: Distances) -> None:
    """Calculates the distances between the shapes

    :param shape_list: List of shapes of which the distances are computed
    :param distances: Contains matrix with distances of descriptors and properties to save to
    """
    j = 0
    for property_name in Properties.NAMES:
        # Fill
        vectors: np.ndarray = np.zeros(shape=(NR_SHAPES, 20))
        for i in range(len(shape_list)):
            vectors[i] = shape_list[i].properties.__getattribute__(property_name)

        # Create all combinations
        combinations = np.array(np.meshgrid(np.arange(NR_SHAPES), np.arange(NR_SHAPES))).T.reshape(-1, 2)
        property_combinations = vectors[combinations]
        relative_properties = property_combinations[:, 0] - property_combinations[:, 1]
        relative_properties_matrix = relative_properties.reshape(380, 380, -1)
        # euclidian_distances = np.linalg.norm(relative_properties_matrix, axis=2)

        # Set values to distances matrix
        for i in range(20):
            distances.matrix[len(Descriptors.NAMES) + j * 20 + i] = relative_properties_matrix[:, :, i]
        j += 1


def calc_emd_distance_matrix(shape_list: [Shape], attribute: str) -> np.ndarray:
    """Calculates the earths mover distance of all the shapes and saves it to a matrix

    :param shape_list: List of shapes to calculate the EMD of
    :param attribute: The histogram feature to compute the EMD for
    :return: The distances between the shapes
    """
    result_matrix = np.full((NR_SHAPES, NR_SHAPES), 0.0)

    i = 0
    for shape in tqdm(shape_list):
        result_matrix[i] = calc_emd_distance_row(shape_list, shape, attribute)
        i += 1

    return result_matrix


def calc_emd_distance_row(shape_list: [Shape], shape: Shape, attribute: str) -> np.ndarray:
    """Gets the EMD for a list of shapes compared to the given shape

    :param shape_list: List of shapes to compute EMD for
    :param shape: Query shape which is h
    :param attribute: Attribute to calculate the EMD over
    :return: The row in the EMD distance matrix
    """
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

    result_row = np.full(NR_SHAPES, 0.0)
    # result_matrix = np.zeros((NR_SHAPES, NR_SHAPES), dtype=float)
    i = 0
    query_arr = shape.properties.__getattribute__(attribute)
    for shape_1 in tqdm(shape_list):
        arr1 = shape_1.proparrerties.__getattribute__(attribute)
        val = emd(arr1, query_arr, distance_matrix)
        result_row[i] = val
        i += 1

    return result_row


def calc_entropy(shape_dict: dict[str, Shape], attribute: str) -> np.ndarray:
    """Calculates the entropy between all shapes

    :param shape_dict: Contains all values to compute the entropy of
    :param attribute: Attribute to compute the entropy of
    :return: Slice of distances
    """
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
    """Calculates the jensen shannon distances between all shapes in the shape dictionary

    :param shape_dict: The collection of shapes to compute the distances of
    :param attribute: Attribute name to compute the distance of
    :return: Matrix of distances using jensen
    """
    result_matrix = np.full((len(shape_dict), len(shape_dict)), 0.0)
    i = 0

    # Loop through each shape combination
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
    """Computes the euclidian distance of all the shapes

    :param shape_dict: The collection of shapes to compute the distances of
    :param attribute: Attribute name to compute the distance of
    :return: Matrix of the euclidean distances
    """
    result_matrix = np.full((len(shape_dict), len(shape_dict)), 0.0)
    i = 0

    # Loop through each shape combination
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

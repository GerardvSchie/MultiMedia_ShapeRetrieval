from copy import deepcopy
import random
from tqdm import tqdm

from src.plot.confusion_matrix import ConfusionMatrixPlotter
from src.object.distances import Distances
from src.util.configs import *


def compute_accuracy(distances: Distances, weight_vector: np.array, knn_mode: bool) -> float:
    """Computes accuracy of the guesses using the weights

    :param distances: Distances of each slice
    :param weight_vector: Weight that is assigned to each distance
    :return: Accuracy of the guesses using k=10
    """
    if not knn_mode:
        weighted_distances = distances.weighted_distances(weight_vector)
    else:
        weighted_distances = distances.weighted_knn_distances(weight_vector)

    confusion_matrix = ConfusionMatrixPlotter.calc_confusion_matrix(weighted_distances, k=10)
    accuracy = np.mean(confusion_matrix.diagonal())
    return float(accuracy)


def print_results(accuracy: float, weight_vector: np.array) -> None:
    """Prints results in standard format

    :param accuracy: Accuracy of the guesses
    :param weight_vector: Weight vector used to produce the accuracy
    """
    print('accuracy:', accuracy, 'vector', str(weight_vector).replace('\n', ''))


def hand_selected(distances: Distances, knn_mode: bool) -> None:
    """Use manually selected weight vector and show the accuracy

    :param distances: Distances of each index in vector
    :param knn_mode: Whether to strictly use euclidian distances
    """
    # Doesn't use the properties
    selected_vector = np.array([1.5, 0.4, 1.3, 0.3, 1.7, 0., 0.2, 0.1, 0.5, 0., 0., 0., 0., 0.])
    accuracy = compute_accuracy(distances, selected_vector, knn_mode)
    print_results(accuracy, selected_vector)


def hyperparameter_tuning(distances: Distances) -> None:
    """Perform hyperparameter tuning and discover

    :param distances: Distances between all shapes in 3D matrix, per descriptor
    """
    params = {
        'surface_area': [1.3, 1.5, 1.7],
        'compactness': [0.3, 0.5, 0.7],
        'sphericity': [1.4, 1.6, 1.8],
        'rectangularity': [0.4, 0.6, 0.8],
        'convexity': [1.0, 1.3, 1.6],
        'diameter': [0.1, 0.2, 0.4],
        'eccentricity': [0.2, 0.3, 0.6],
        'major_eccentricity': [0.2, 0.3, 0.4],
        'minor_eccentricity': [0.1, 0.2, 0.3],
    }

    # Stores best results
    best_vector = None
    best_accuracy = 0

    # The total number of combinations that will get checked
    nr_values = 1
    for param in params:
        nr_values *= len(params[param])

    # Use all values of all component in parameters
    with tqdm(total=nr_values) as pbar:
        for surface_area in tqdm(params['surface_area']):
            for compactness in params['compactness']:
                for sphericity in params['sphericity']:
                    for rectangularity in params['rectangularity']:
                        for convexity in params['convexity']:
                            for diameter in params['diameter']:
                                for eccentricity in params['eccentricity']:
                                    for major_eccentricity in params['major_eccentricity']:
                                        for minor_eccentricity in params['minor_eccentricity']:
                                            # Doesn't yet use the
                                            weight_vector = np.array([surface_area, compactness, sphericity, rectangularity,
                                                                      convexity, diameter, eccentricity, major_eccentricity, minor_eccentricity,
                                                                      0, 0, 0, 0, 0])

                                            # Computes accuracy
                                            accuracy = compute_accuracy(distances, weight_vector)

                                            # If accuracy improves print improved result
                                            if accuracy > best_accuracy:
                                                best_accuracy = accuracy
                                                best_vector = weight_vector
                                                print_results(best_accuracy, best_vector)

                                            # Update loading bar
                                            pbar.update()

    # Print the best results found after hyperparameter tuning
    print('Best results after hyperparameter tuning')
    print_results(best_accuracy, best_vector)


def local_search(distances: Distances, initial_vector: np.array, knn_mode: bool) -> None:
    """Adjust vector automatically by adjusting weights of the components

    :param distances: Contains matrix that contains distance of each component of the vector
    :param initial_vector: Initial state to perform local search from
    :param knn_mode: Strictly uses euclidian distance
    """
    best_vector = initial_vector
    best_accuracy = compute_accuracy(distances, initial_vector, knn_mode)

    # Perform 5000 iterations during local search
    iteration = 0
    iterations_without_improvement = 0
    while iteration < 5000:
        # So we do not change the original vector
        weight_vector = deepcopy(best_vector)

        # Between +-10% for each component
        nr_picks = min(int(iterations_without_improvement / 100) + 1, len(Distances.NAMES))
        indexes = np.random.choice(range(len(Distances.NAMES)), nr_picks, replace=False)
        for i in indexes:
            weight_vector[i] *= (1 + random.uniform(-0.2, 0.2))

        # Get accuracy of new vector
        accuracy = compute_accuracy(distances, weight_vector, knn_mode)

        # If better, update best solution
        if accuracy > best_accuracy:
            best_accuracy = accuracy
            best_vector = weight_vector
            print_results(best_accuracy, best_vector)
            iterations_without_improvement = 0

        # Next iteration
        iteration += 1
        iterations_without_improvement += 1

    # Print out best results
    print('Best results after local search:')
    print_results(best_accuracy, best_vector)
    # best accuracy: 0.6702631578947369 vector [1.3 0.3 1.6 0.8 1.3 0.1 0.6 0.4 0.2 0.  0.  0.  0.  0. ]

    # accuracy: 0.6815789473684211 vector [ 1.17440188  0.29713889  1.64954493  1.07265445  1.13989037  0.14093051  0.58413028  0.4734819   0.1261543   5.01591765  3.70181446  2.01307203  7.08781804 10.51297132]


def main(knn_mode: bool):
    """Main method for hyperparameter tuning and local search
    Tries to optimize accuracy of the query
    """
    # Get the distances for each component
    if knn_mode:
        distances = Distances(os.path.join(DATABASE_DIR, DATABASE_KNN_DISTANCES_FILENAME))
    else:
        distances = Distances(os.path.join(DATABASE_DIR, DATABASE_DISTANCES_FILENAME))

    # Test the various methods
    hand_selected(distances, knn_mode)

    # Hyperparameter tuning takes a long time to execute
    # hyperparameter_tuning(distances, knn_mode)

    best_vector = np.array([1.3, 0.3, 1.6, 0.8, 1.3, 0.1, 0.6, 0.4, 0.2, 0., 0., 0., 0., 0.])
    best_vector = np.array(
        [1.0013151, 0.30078011, 1.44363058, 0.88030667, 0.97392208, 0.13535301, 0.53812947, 0.44469075, 0.14004997, 7,
         7, 7, 7, 5])
    best_vector = np.array(
        [1.0013151, 0.30078011, 1.44363058, 0.88030667, 0.97392208, 0.13535301, 0.53812947, 0.44469075, 0.14004997,
         5.22630039, 5.67574125, 2.65753931, 7.66481085, 5.37005448])
    best_vector = np.array(
        [1.0013151, 0.30078011, 1.44363058, 0.88030667, 0.97392208, 0.13535301, 0.53812947, 0.44469075, 0.14004997,
         4.97262054, 3.5104284, 1.80775629, 8.25943989, 7.6972006])

    best_vector = np.array(
        [1.0013151, 0.30078011, 1.44363058, 0.88030667, 0.97392208, 0.13535301, 0.53812947, 0.44469075, 0.14004997,
         4.97262054, 3.5104284, 1.80775629, 8.25943989, 9.6972006])

    if knn_mode:
        best_vector = KNN_WEIGHT_VECTOR
        # accuracy: 0.7107894736842105 vector [ 1.00914947  0.50335688  1.69586111  1.34745224  1.82110232  0.10521264  0.60581433  0.325439    0.11662168  2.69578308  3.08456191  0.96369678  1.7059177  15.38864842]
    else:
        best_vector = np.array([1.17440188, 0.29713889, 1.64954493, 1.07265445, 1.13989037, 0.14093051, 0.58413028,
                                0.48224995, 0.1261543, 5.01591765, 3.75394319, 2.01307203, 7.63732949, 9.87755763])

    local_search(distances, best_vector, knn_mode)


#accuracy: 0.7071052631578948 vector [ 1.26871346  0.4905116   2.07605749  1.1932621   1.74392193  0.13197155  0.52970982  0.37158661  0.12136592  4.29253166  3.16317135  1.23314089  1.50789865 10.01651088]

if __name__ == '__main__':
    main(knn_mode=True)

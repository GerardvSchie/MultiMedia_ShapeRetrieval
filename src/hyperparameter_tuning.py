from copy import deepcopy
import random

from tqdm import tqdm

from src.plot.confusion_matrix import ConfusionMatrixPlotter
from src.object.distances import Distances
from src.util.configs import *


def compute_accuracy(distances: Distances, weight_vector: np.array) -> float:
    """Computes accuracy of the guesses using the weights

    :param distances: Distances of each slice
    :param weight_vector: Weight that is assigned to each distance
    :return: Accuracy of the guesses using k=10
    """
    weighted_distances = distances.weighted_distances(weight_vector)
    confusion_matrix = ConfusionMatrixPlotter.calc_confusion_matrix(weighted_distances, k=10)
    accuracy = np.mean(confusion_matrix.diagonal())
    return float(accuracy)


def print_results(accuracy: float, weight_vector: np.array) -> None:
    """Prints results in standard format

    :param accuracy: Accuracy of the guesses
    :param weight_vector: Weight vector used to produce the accuracy
    """
    print('accuracy:', accuracy, 'vector', str(weight_vector).replace('\n', ''))


def hand_selected(distances: Distances) -> None:
    """Use manually selected weight vector and show the accuracy

    :param distances: Distances of each index in vector
    """
    # Doesn't use the properties
    selected_vector = np.array([1.5, 0.4, 1.3, 0.3, 1.7, 0., 0.2, 0.1, 0.5, 0., 0., 0., 0., 0.])
    accuracy = compute_accuracy(distances, selected_vector)
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


def local_search(distances: Distances, initial_vector: np.array) -> None:
    """Adjust vector automatically by adjusting weights of the components

    :param distances: Contains matrix that contains distance of each component of the vector
    :param initial_vector: Initial state to perform local search from
    """
    best_vector = initial_vector
    best_accuracy = compute_accuracy(distances, initial_vector)

    # Perform 5000 iterations during local search
    iteration = 0
    while iteration < 5000:
        # So we do not change the original vector
        weight_vector = deepcopy(best_vector)

        # Between +-10% for each component
        for i in range(len(Distances.NAMES)):
            weight_vector[i] *= (1 + random.uniform(-0.1, 0.1))

        # Get accuracy of new vector
        accuracy = compute_accuracy(distances, weight_vector)

        # If better, update best solution
        if accuracy > best_accuracy:
            best_accuracy = accuracy
            best_vector = weight_vector
            print_results(best_accuracy, best_vector)

        # Next iteration
        iteration += 1

    # Print out best results
    print('Best results after local search:')
    print_results(best_accuracy, best_vector)
    # best accuracy: 0.6702631578947369 vector [1.3 0.3 1.6 0.8 1.3 0.1 0.6 0.4 0.2 0.  0.  0.  0.  0. ]

    # accuracy: 0.6763157894736843 vector [1.0013151  0.30078011 1.44363058 0.88030667 0.97392208 0.13535301 0.53812947 0.44469075 0.14004997 0.         0.         0. 0.         0.        ] iteration 1739
    # accuracy: 0.6860526315789474 vector [0.84946192 0.52634137 0.97686527 0.8570737  0.79787693 0.09474074 0.41083903 0.27356298 0.10522074 5.22630039 5.67574125 2.65753931 7.66481085 5.37005448] iteration 210
    # accuracy: 0.6897368421052632 vector [1.53671594 0.36237169 1.46250151 1.24950136 1.35252345 0.1534592 0.62359625 0.53501483 0.13396279 4.97262054 3.5104284  1.80775629 8.25943989 7.6972006 ]

    # accuracy: 0.6926315789473684 vector [0.59957526 0.41485836 1.14837189 0.8737181  1.17632872 0.12859756 0.43187859 0.30701326 0.20125682 4.3040526  2.40889516 1.39163004 6.64441423 9.02004084] iteration 909
    # accuracy: 0.6926315789473685 vector [0.63760714 0.42292345 1.22216305 0.9573012  1.11486596 0.13102545 0.39686013 0.31734303 0.21730884 4.40158501 2.6044959  1.5177154 6.24597882 8.3256162 ] iteration 1042
    # accuracy: 0.6928947368421052 vector [0.58423243 0.40810507 1.25033164 0.95827973 1.12384264 0.13254815 0.4053965  0.29668712 0.19888426 4.63333763 2.43744218 1.39672426 6.66946949 8.05046796] iteration 1110
    # accuracy: 0.6931578947368421 vector [0.59073971 0.41892132 1.15142093 0.8846405  1.06883754 0.12974587 0.42166752 0.27647947 0.20706151 4.31139582 2.53083674 1.34090725 6.81671266 8.77233668] iteration 1197
    # accuracy: 0.6939473684210526 vector [0.63526925 0.44627614 1.22175252 0.90124816 1.15243963 0.13149682 0.44591687 0.25190178 0.19053711 4.0382616  2.35425451 1.45513358 7.05197262 9.24651963] iteration 1301


def main():
    # Get the distances for each component
    distances = Distances(os.path.join(DATABASE_DIR, DATABASE_DISTANCES_FILENAME))

    # Test the various methods
    hand_selected(distances)
    # hyperparameter_tuning(distances)

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

    # After fixing the range of A3
    best_vector = np.array([1.17440188, 0.29713889, 1.64954493, 1.07265445, 1.13989037, 0.14093051, 0.58413028,
                            0.48224995, 0.1261543, 5.01591765, 3.75394319, 2.01307203, 7.63732949, 9.87755763])

    local_search(distances, best_vector)


if __name__ == '__main__':
    main()

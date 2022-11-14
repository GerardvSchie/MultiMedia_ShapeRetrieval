from copy import deepcopy
import random

from tqdm import tqdm

from src.object.descriptors import Descriptors
from src.plot.confusion_matrix import ConfusionMatrixPlotter
from src.object.distances import Distances
from src.util.configs import *

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

distances = Distances(os.path.join(DATABASE_DIR, DATABASE_DISTANCES_FILENAME))

nr_values = 1
for param in params:
    nr_values *= len(params[param])

print('combinations:', nr_values)

best_accuracy = 0
best_vector = None

# weighted_distances = distances.weighted_distances(WEIGHT_VECTOR)
# confusion_matrix = ConfusionMatrixPlotter.calc_confusion_matrix(weighted_distances)
# accuracy = np.mean(confusion_matrix.diagonal())
#
# # before accuracy: 0.6273684210526315 vector [1.5 0.4 1.3 0.3 1.7 0.  0.2 0.1 0.5 0.  0.  0.  0.  0. ]
# print('\nbefore accuracy:', accuracy, 'vector', WEIGHT_VECTOR)

#
# with tqdm(total=nr_values) as pbar:
#     for surface_area in tqdm(params['surface_area']):
#         for compactness in params['compactness']:
#             for sphericity in params['sphericity']:
#                 for rectangularity in params['rectangularity']:
#                     for convexity in params['convexity']:
#                         for diameter in params['diameter']:
#                             for eccentricity in params['eccentricity']:
#                                 for major_eccentricity in params['major_eccentricity']:
#                                     for minor_eccentricity in params['minor_eccentricity']:
#                                         weight_vector = np.array([surface_area, compactness, sphericity, rectangularity,
#                                                                   convexity, diameter, eccentricity, major_eccentricity, minor_eccentricity,
#                                                                   0, 0, 0, 0, 0])
#
#                                         weighted_distances = distances.weighted_distances(weight_vector)
#                                         confusion_matrix = ConfusionMatrixPlotter.calc_confusion_matrix(weighted_distances)
#                                         accuracy = np.mean(confusion_matrix.diagonal())
#
#                                         if accuracy > best_accuracy:
#                                             best_accuracy = accuracy
#                                             best_vector = weight_vector
#                                             print('\naccuracy:', accuracy, 'vector', weight_vector)
#
#                                         pbar.update()

#   7%|▋         | 1322/19683 [03:07<44:00,  6.95it/s]
# best accuracy: 0.6702631578947369 vector [1.3 0.3 1.6 0.8 1.3 0.1 0.6 0.4 0.2 0.  0.  0.  0.  0. ]
best_vector = np.array([1.3, 0.3, 1.6, 0.8, 1.3, 0.1, 0.6, 0.4, 0.2, 0., 0., 0., 0., 0.])
best_vector = np.array([1.0013151, 0.30078011, 1.44363058, 0.88030667, 0.97392208, 0.13535301, 0.53812947, 0.44469075, 0.14004997, 7, 7, 7, 7, 5])
best_vector = np.array([1.0013151, 0.30078011, 1.44363058, 0.88030667, 0.97392208, 0.13535301, 0.53812947, 0.44469075, 0.14004997, 5.22630039, 5.67574125, 2.65753931, 7.66481085, 5.37005448])
best_vector = np.array([1.0013151, 0.30078011, 1.44363058, 0.88030667, 0.97392208, 0.13535301, 0.53812947, 0.44469075, 0.14004997, 4.97262054, 3.5104284, 1.80775629, 8.25943989, 7.6972006])

# accuracy: 0.6736842105263158 vector [1.30685535 0.29515438 1.54160849 0.86606538 1.22091153 0.1
#  0.6        0.43032017 0.21779412 0.         0.         0.
#  0.         0.        ] iteration 48

# accuracy: 0.6726315789473685 vector [1.3        0.28461165 1.6        0.83809563 1.30791396 0.08391926 0.6        0.4        0.22529415 0.         0.         0. 0.         0.        ] iteration 1438

iteration = 0
while iteration < 5000:
    weight_vector = deepcopy(best_vector)

    # Between +-20% for each one
    for i in range(len(Distances.NAMES)):
        weight_vector[i] *= (1 + random.uniform(-0.1, 0.1))

    weighted_distances = distances.weighted_distances(weight_vector)
    confusion_matrix = ConfusionMatrixPlotter.calc_confusion_matrix(weighted_distances)
    accuracy = np.mean(confusion_matrix.diagonal())

    if accuracy > best_accuracy:
        best_accuracy = accuracy
        best_vector = weight_vector
        print('\naccuracy:', accuracy, 'vector', str(weight_vector).replace('\n', ''), 'iteration', iteration)

    iteration += 1

print('\nbest accuracy:', best_accuracy, 'best vector', best_vector)

# accuracy: 0.6763157894736843 vector [1.0013151  0.30078011 1.44363058 0.88030667 0.97392208 0.13535301 0.53812947 0.44469075 0.14004997 0.         0.         0. 0.         0.        ] iteration 1739
# accuracy: 0.6860526315789474 vector [0.84946192 0.52634137 0.97686527 0.8570737  0.79787693 0.09474074 0.41083903 0.27356298 0.10522074 5.22630039 5.67574125 2.65753931 7.66481085 5.37005448] iteration 210
# accuracy: 0.6897368421052632 vector [1.53671594 0.36237169 1.46250151 1.24950136 1.35252345 0.1534592 0.62359625 0.53501483 0.13396279 4.97262054 3.5104284  1.80775629 8.25943989 7.6972006 ]

# Subsequent run
# accuracy: 0.6926315789473684 vector [0.59957526 0.41485836 1.14837189 0.8737181  1.17632872 0.12859756 0.43187859 0.30701326 0.20125682 4.3040526  2.40889516 1.39163004 6.64441423 9.02004084] iteration 909
# accuracy: 0.6926315789473685 vector [0.63760714 0.42292345 1.22216305 0.9573012  1.11486596 0.13102545 0.39686013 0.31734303 0.21730884 4.40158501 2.6044959  1.5177154 6.24597882 8.3256162 ] iteration 1042
# accuracy: 0.6928947368421052 vector [0.58423243 0.40810507 1.25033164 0.95827973 1.12384264 0.13254815 0.4053965  0.29668712 0.19888426 4.63333763 2.43744218 1.39672426 6.66946949 8.05046796] iteration 1110
# accuracy: 0.6931578947368421 vector [0.59073971 0.41892132 1.15142093 0.8846405  1.06883754 0.12974587 0.42166752 0.27647947 0.20706151 4.31139582 2.53083674 1.34090725 6.81671266 8.77233668] iteration 1197
# accuracy: 0.6939473684210526 vector [0.63526925 0.44627614 1.22175252 0.90124816 1.15243963 0.13149682 0.44591687 0.25190178 0.19053711 4.0382616  2.35425451 1.45513358 7.05197262 9.24651963] iteration 1301
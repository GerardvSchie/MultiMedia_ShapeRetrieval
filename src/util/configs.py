"""
This file contains global configurations for the application
General settings, weights, and paths are included
"""

import os
import numpy as np

# General settings
NR_VERTICES = 10000
NR_SHAPES = 380
NR_CATEGORIES = 19

# Weight vector
DESCRIPTOR_WEIGHT_VECTOR = np.array([1.17440188, 0.29713889, 1.64954493, 1.07265445, 1.13989037, 0.14093051, 0.58413028, 0.48224995, 0.1261543])
PROPERTIES_WEIGHT_VECTOR = np.array([5.01591765, 3.75394319, 2.01307203, 7.63732949, 9.87755763])
WEIGHT_VECTOR = np.append(DESCRIPTOR_WEIGHT_VECTOR, PROPERTIES_WEIGHT_VECTOR)
WEIGHT_VECTOR_STR = str(np.round(WEIGHT_VECTOR, 2))

# Shape paths
FILENAME_ORIGINAL = 'original.ply'
FILENAME_NORMALIZED_PCD = 'normalized_v2.pcd'
FILENAME_NORMALIZED_PLY = 'normalized_v2.ply'

# Database paths
DATABASE_DIR = 'data/database'
DATABASE_ORIGINAL_DIR = os.path.join(DATABASE_DIR, 'original')
DATABASE_NORMALIZED_DIR = os.path.join(DATABASE_DIR, 'normalized')

DATABASE_FEATURES_FILENAME = 'features.csv'
DATABASE_DESCRIPTORS_FILENAME = 'descriptors.csv'
DATABASE_DESCRIPTORS_INI = 'descriptors.ini'
DATABASE_NORMALIZED_DESCRIPTORS_FILENAME = 'descriptors_normalized.csv'
DATABASE_PROPERTIES_FILENAME = 'properties.csv'
DATABASE_NORMALIZED_PROPERTIES_FILENAME = 'properties_normalized.csv'
DATABASE_DISTANCES_FILENAME = 'distances.npy'
DATABASE_TSNE_FILENAME = 'tsne_coordinates.npy'

# Plot paths
PLOT_DIR = 'plots'

PLOT_FEATURES_DIR = os.path.join(PLOT_DIR, 'features')
PLOT_ORIGINAL_FEATURES_DIR = os.path.join(PLOT_FEATURES_DIR, 'original')
PLOT_REFINED_FEATURES_DIR = os.path.join(PLOT_FEATURES_DIR, 'refined')

PLOT_DESCRIPTORS_DIR = os.path.join(PLOT_DIR, 'descriptors')
PLOT_REFINED_DESCRIPTORS_DIR = os.path.join(PLOT_DESCRIPTORS_DIR, 'refined')
PLOT_NORMALIZED_DESCRIPTORS_DIR = os.path.join(PLOT_DESCRIPTORS_DIR, 'normalized')

PLOT_DISTANCES_DIR = os.path.join(PLOT_DIR, 'distances')
PLOT_DESCRIPTORS_DISTANCES_DIR = os.path.join(PLOT_DISTANCES_DIR, 'descriptors')

PLOT_OUTLIERS_DIR = os.path.join(PLOT_DIR, 'outliers')
PLOT_PROPERTIES_DIR = os.path.join(PLOT_DIR, 'properties')
PLOT_CONFUSION_MATRICES = os.path.join(PLOT_DIR, 'confusion_matrices')

# Query results
NR_RESULTS = 20

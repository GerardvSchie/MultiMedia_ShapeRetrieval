import os
import numpy as np

# General settings
NR_VERTICES = 10000
NR_SHAPES = 380
NR_CATEGORIES = 19

# Querying
# DESCRIPTOR_WEIGHT_VECTOR = np.array([1.5, 0.4, 1.3, 0.3, 1.7, 0, 0.2, 0.1, 0.5])
# PROPERTIES_WEIGHT_VECTOR = np.array([8, 10, 10, 10, 4])
# PROPERTIES_WEIGHT_VECTOR = np.array([0, 0, 0, 0, 0])

DESCRIPTOR_WEIGHT_VECTOR = np.array([0.63526925, 0.44627614, 1.22175252, 0.90124816, 1.15243963, 0.13149682, 0.44591687, 0.25190178, 0.19053711])
PROPERTIES_WEIGHT_VECTOR = np.array([4.0382616, 2.35425451, 1.45513358, 7.05197262, 9.24651963])

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

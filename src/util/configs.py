import os

# General settings
NR_VERTICES = 10000

# Paths
FILENAME_ORIGINAL = 'original.ply'
# FILENAME_NORMALIZED_PCD = 'normalized.pcd'
# FILENAME_NORMALIZED_PLY = 'normalized.ply'
# FILENAME_REFINED = 'refined.ply'

FILENAME_NORMALIZED_PCD = 'normalized_v2.pcd'
FILENAME_NORMALIZED_PLY = 'normalized_v2.ply'

# Database paths
DATABASE_DIR = 'data/database'
DATABASE_ORIGINAL_DIR = os.path.join(DATABASE_DIR, 'original')
DATABASE_REFINED_DIR = os.path.join(DATABASE_DIR, 'refined')
DATABASE_NORMALIZED_DIR = os.path.join(DATABASE_DIR, 'normalized')

DATABASE_FEATURES_FILENAME = 'features.csv'
DATABASE_DESCRIPTORS_FILENAME = 'descriptors.csv'
DATABASE_DESCRIPTORS_INI = 'descriptors.ini'
DATABASE_NORMALIZED_DESCRIPTORS_FILENAME = 'descriptors_normalized.csv'

# Plot paths
PLOT_DIR = 'plots'

PLOT_FEATURES_DIR = os.path.join(PLOT_DIR, 'features')
PLOT_ORIGINAL_FEATURES_DIR = os.path.join(PLOT_FEATURES_DIR, 'original')
PLOT_REFINED_FEATURES_DIR = os.path.join(PLOT_FEATURES_DIR, 'refined')

PLOT_DESCRIPTORS_DIR = os.path.join(PLOT_DIR, 'descriptors')
PLOT_REFINED_DESCRIPTORS_DIR = os.path.join(PLOT_DESCRIPTORS_DIR, 'refined')
PLOT_NORMALIZED_DESCRIPTORS_DIR = os.path.join(PLOT_DESCRIPTORS_DIR, 'normalized')

PLOT_DISTANCES_DIR = os.path.join(PLOT_DIR, 'distances')

PLOT_OUTLIERS_DIR = os.path.join(PLOT_DIR, 'outliers')

PLOT_PROPERTIES_DIR = os.path.join(PLOT_DIR, 'properties')

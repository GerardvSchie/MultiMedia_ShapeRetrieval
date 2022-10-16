import os
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

import src.util.io
import src.plot.util as util
from src.object.features.shape_features import ShapeFeatures

# Python can't convert variable names to string.
MESH_FACES = 'Mesh nr. faces'
MESH_VERTICES = 'Mesh nr. vertices'


class FeatureDistributionPlotter:
    @staticmethod
    def plot_features(data: [ShapeFeatures]):
        # hi = map(key=lambda a: a.mesh, data)
        FeatureDistributionPlotter.plot(data, ['normalization_features', 'distance_to_center'], 'Distance to center')
        FeatureDistributionPlotter.plot(data, ['normalization_features', 'scale'], 'Scale')
        FeatureDistributionPlotter.plot(data, ['normalization_features', 'alignment'], 'Alignment')
        FeatureDistributionPlotter.plot(data, ['normalization_features', 'flip'], 'Correctly directed axes')
        FeatureDistributionPlotter.plot(data, ['mesh_features', 'nr_faces'], 'Number of faces')
        FeatureDistributionPlotter.plot(data, ['mesh_features', 'nr_vertices'], 'Number of vertices')

    @staticmethod
    def plot(data: [ShapeFeatures], feature_names: [str], title: str):
        # Choose a backend for matplotlib
        matplotlib.use('TkAgg')

        for feature_name in feature_names:
            data = [item.__getattribute__(feature_name) for item in data]

        n, bins, patches = plt.hist(data, bins=100, range=(0, max(data)), weights=np.full(len(data), 1 / len(data)))

        shape_closest_to_mean = src.util.plot.closestValue(data, np.mean(data))
        for i, bin in enumerate(bins):
            if bin < shape_closest_to_mean:
                continue

            patches[i - 1].set_fc('r')
            break

        # Set titles and parameters
        util.set_params()
        plt.title(f'Shape {title.lower()} distribution', fontdict={'fontsize': util.BIGGER_SIZE})
        plt.xlabel(f'{title}')
        plt.ylabel('Percentage of shapes')

        # Save plot
        util.save_feature_distribution_plt(title, os.path.join('plots/features'))


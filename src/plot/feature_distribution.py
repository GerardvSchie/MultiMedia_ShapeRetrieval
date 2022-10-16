import os
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

import src.util.io
import src.plot.util as util
from src.object.features.shape_features import ShapeFeatures


class FeatureDistributionPlotter:
    @staticmethod
    def plot_features(data: [ShapeFeatures]):
        FeatureDistributionPlotter.histogram_plot(data, ['normalization_features', 'distance_to_center'], 'Distance to center')
        FeatureDistributionPlotter.histogram_plot(data, ['normalization_features', 'scale'], 'Scale')
        FeatureDistributionPlotter.histogram_plot(data, ['normalization_features', 'alignment'], 'Alignment')
        FeatureDistributionPlotter.histogram_plot(data, ['normalization_features', 'flip'], 'Correctly directed axes')
        FeatureDistributionPlotter.histogram_plot(data, ['mesh_features', 'nr_faces'], 'Number of faces')
        FeatureDistributionPlotter.histogram_plot(data, ['mesh_features', 'nr_vertices'], 'Number of vertices')
        FeatureDistributionPlotter.pie_plot(data, ['mesh_features', 'is_watertight'], 'watertight')

    @staticmethod
    def pie_plot(data: [ShapeFeatures], feature_names: [str], title: str):
        # Source: https://matplotlib.org/stable/gallery/pie_and_polar_charts/pie_features.html
        # Choose a backend for matplotlib
        matplotlib.use('TkAgg')

        for feature_name in feature_names:
            data = [item.__getattribute__(feature_name) for item in data]

        n = len(data)
        p = sum(data) / n
        plt.pie([p, 1-p], explode=[0, 0.1], labels=[True, False], autopct='%1.1f%%',
                shadow=True, startangle=90)
        plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

        plt.title(f'Distribution of {title.lower()} shapes', fontdict={'fontsize': util.BIGGER_SIZE})
        util.save_feature_distribution_plt(title, os.path.join('plots/features'))

    @staticmethod
    def histogram_plot(data: [ShapeFeatures], feature_names: [str], title: str):
        # Choose a backend for matplotlib
        matplotlib.use('TkAgg')

        for feature_name in feature_names:
            data = [item.__getattribute__(feature_name) for item in data]

        n = len(data)
        _, bins, patches = plt.hist(data, bins=int(np.ceil(np.sqrt(n))), range=(0, max(data)), weights=np.full(n, 1 / n))

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

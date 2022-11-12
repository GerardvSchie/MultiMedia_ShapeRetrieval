import os
import numpy as np

from src.object.descriptors import Descriptors
from src.plot.util import histogram_plot


class DescriptorDistributionPlotter:
    @staticmethod
    def plot_descriptors(plot_dir: str, data: [Descriptors]):
        for name in Descriptors.NAMES:
            DescriptorDistributionPlotter.numerical_feature(plot_dir, data, [name], name.replace('_', ' ').capitalize())

    @staticmethod
    def numerical_feature(plot_dir: str, data: [Descriptors], feature_names: [str], title: str):
        for feature_name in feature_names:
            data = [item.__getattribute__(feature_name) for item in data]

        plot_path = os.path.join(plot_dir, feature_names[-1].lower() + '.png')
        plot_title = f'Shape {title.lower()} distribution'
        x_label = title
        y_label = 'Percentage of shapes'
        histogram_plot(plot_path, data, plot_title, x_label, y_label, np.min(data))

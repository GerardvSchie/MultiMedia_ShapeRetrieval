import os
import numpy as np

from src.object.descriptors import Descriptors
from src.plot.util import histogram_plot


class DescriptorDistributionPlotter:
    @staticmethod
    def plot_descriptors(plot_dir: str, data: [Descriptors]):
        """Plots all the descriptors in histograms

        :param plot_dir: Directory to save the plots in
        :param data: Descriptor data
        """
        for name in Descriptors.NAMES:
            data = [item.__getattribute__(name) for item in data]

            # Plot path and title
            plot_path = os.path.join(plot_dir, name.lower() + '.png')
            title = name.replace('_', ' ').capitalize()
            plot_title = f'Shape {title.lower()} distribution'

            # Create histogram plot
            histogram_plot(plot_path, data, plot_title, x_label=title, y_label='Percentage of shapes',
                           min_range=np.min(data))

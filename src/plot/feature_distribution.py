import os

from src.object.features.shape_features import ShapeFeatures
from src.plot.util import histogram_plot, pie_plot


class FeatureDistributionPlotter:
    @staticmethod
    def plot_features(plot_dir: str, data: [ShapeFeatures]) -> None:
        """Plot a few of the features data

        :param plot_dir: Directory to save the plots in
        :param data: Data to plot
        """
        FeatureDistributionPlotter.numerical_feature(plot_dir, data, ['normalization_features', 'distance_to_center'], 'Distance to center')
        FeatureDistributionPlotter.numerical_feature(plot_dir, data, ['normalization_features', 'scale'], 'Scale')
        FeatureDistributionPlotter.numerical_feature(plot_dir, data, ['normalization_features', 'alignment'], 'Alignment')
        FeatureDistributionPlotter.numerical_feature(plot_dir, data, ['normalization_features', 'flip'], 'Correctly directed axes')
        FeatureDistributionPlotter.numerical_feature(plot_dir, data, ['mesh_features', 'nr_faces'], 'Number of faces')
        FeatureDistributionPlotter.numerical_feature(plot_dir, data, ['mesh_features', 'nr_vertices'], 'Number of vertices')
        FeatureDistributionPlotter.category_feature(plot_dir, data, ['mesh_is_watertight'], 'watertight')

    @staticmethod
    def numerical_feature(plot_dir: str, data: [ShapeFeatures], feature_names: [str], title: str) -> None:
        """Plots numerical values in histogram plot

        :param plot_dir: Directory name to save plot to
        :param data: Numerical data to plot in histogram
        :param feature_names: Name of the feature
        :param title: Title of the plot
        """
        for feature_name in feature_names:
            data = [item.__getattribute__(feature_name) for item in data]

        # Path of the plot
        plot_path = os.path.join(plot_dir, feature_names[-1].lower() + '.png')
        plot_title = f'Shape {title.lower()} distribution'
        histogram_plot(plot_path, data, plot_title, x_label=title, y_label='Percentage of shapes')

    @staticmethod
    def category_feature(plot_dir: str, data: [ShapeFeatures], feature_names: [str], title: str) -> None:
        """Plots a categorical feature into a pie plot

        :param plot_dir: Directory to save plot in
        :param data: Data to plot
        :param feature_names: Name of the feature that is plotted
        :param title: Title of the plot
        """
        for feature_name in feature_names:
            data = [item.__getattribute__(feature_name) for item in data]

        # Path of plot and create it
        plot_path = os.path.join(plot_dir, feature_names[-1].lower() + '.png')
        plot_title = f'Distribution of {title.lower()} shapes'
        pie_plot(plot_path, data, plot_title)

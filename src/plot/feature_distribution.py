import os

from src.object.features.shape_features import ShapeFeatures
from src.plot.util import histogram_plot, pie_plot


class FeatureDistributionPlotter:
    @staticmethod
    def plot_features(plot_dir: str, data: [ShapeFeatures]):
        FeatureDistributionPlotter.numerical_feature(plot_dir, data, ['normalization_features', 'distance_to_center'], 'Distance to center')
        FeatureDistributionPlotter.numerical_feature(plot_dir, data, ['normalization_features', 'scale'], 'Scale')
        FeatureDistributionPlotter.numerical_feature(plot_dir, data, ['normalization_features', 'alignment'], 'Alignment')
        FeatureDistributionPlotter.numerical_feature(plot_dir, data, ['normalization_features', 'flip'], 'Correctly directed axes')
        FeatureDistributionPlotter.numerical_feature(plot_dir, data, ['mesh_features', 'nr_faces'], 'Number of faces')
        FeatureDistributionPlotter.numerical_feature(plot_dir, data, ['mesh_features', 'nr_vertices'], 'Number of vertices')
        FeatureDistributionPlotter.category_feature(plot_dir, data, ['mesh_is_watertight'], 'watertight')

    @staticmethod
    def numerical_feature(plot_dir: str, data: [ShapeFeatures], feature_names: [str], title: str):
        for feature_name in feature_names:
            data = [item.__getattribute__(feature_name) for item in data]

        plot_path = os.path.join(plot_dir, feature_names[-1].lower() + '.png')
        plot_title = f'Shape {title.lower()} distribution'
        x_label = title
        y_label = 'Percentage of shapes'
        histogram_plot(plot_path, data, plot_title, x_label, y_label)

    @staticmethod
    def category_feature(plot_dir: str, data: [ShapeFeatures], feature_names: [str], title: str):
        for feature_name in feature_names:
            data = [item.__getattribute__(feature_name) for item in data]

        plot_path = os.path.join(plot_dir, feature_names[-1].lower() + '.png')
        plot_title = f'Distribution of {title.lower()} shapes'
        pie_plot(plot_path, data, plot_title)

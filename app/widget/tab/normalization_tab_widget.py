from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout
from PyQt6.QtGui import QWindow

from app.widget.normalization_features_widget import NormalizationFeaturesWidget
from app.widget.util import color_widget
from app.widget.settings_widget import SettingsWidget
from app.widget.features_widget import FeaturesWidget
from app.widget.visualization_widget import VisualizationWidget

from src.object.settings import Settings
from app.util.os import IsMacOS
from src.pipeline.feature_extractor import FeatureExtractor
from src.pipeline.normalization_feature_extractor import NormalizationFeatureExtractor
from src.pipeline.normalization import Normalizer


class NormalizationTabWidget(QWidget):
    def __init__(self):
        super(NormalizationTabWidget, self).__init__()
        color_widget(self, [0, 255, 0])

        # Left panel
        self.settings: Settings = Settings()
        self.settings_widget = SettingsWidget(self.settings)
        self.features_widget_1 = FeaturesWidget()

        # Widget 1
        self.scene_widget_1 = VisualizationWidget(self.settings)
        if not IsMacOS:
            window_1 = QWindow.fromWinId(self.scene_widget_1.hwnd)
            window_container_1 = self.createWindowContainer(window_1, self.scene_widget_1)

        # Widget 2
        self.scene_widget_2 = VisualizationWidget(self.settings)
        if not IsMacOS:
            window_2 = QWindow.fromWinId(self.scene_widget_2.hwnd)
            window_container_2 = self.createWindowContainer(window_2, self.scene_widget_2)

        # Right panel
        self.normalization_widget = NormalizationFeaturesWidget()
        self.features_widget_2 = FeaturesWidget()

        # Connect the settings to the widget
        self.scene_widgets = [self.scene_widget_1, self.scene_widget_2]
        self.settings_widget.connect_visualizers(self.scene_widgets)

        # Assign scene widget here since that covers entire gui
        left_layout = QVBoxLayout()
        left_layout.addWidget(self.settings_widget)
        left_layout.addWidget(self.features_widget_1)

        right_layout = QVBoxLayout()
        right_layout.addWidget(self.normalization_widget)
        right_layout.addWidget(self.features_widget_2)

        layout = QHBoxLayout(self)
        layout.addLayout(left_layout)

        if not IsMacOS:
            layout.addWidget(window_container_1)
            layout.addWidget(window_container_2)

        layout.addLayout(right_layout)
        self.setLayout(layout)

    def load_shape(self, file_path: str):
        # First mesh
        self.scene_widgets[0].load_shape(file_path)
        FeatureExtractor.extract_features(self.scene_widgets[0].shape)
        # NormalizationFeatureExtractor.extract_normalization_features(self.scene_widgets[0].shape)
        self.features_widget_1.update_widget(self.scene_widgets[0].shape.features)

        # Normalized mesh with 3000 points
        self.scene_widgets[1].load_shape(file_path)
        self.scene_widgets[1].clear()

        # self.scene_widgets[1].shape.geometries.point_cloud = self.scene_widgets[1].shape.geometries.mesh.sample_points_poisson_disk(3000)
        # shape.geometries.point_cloud = shape.geometries.mesh.sample_points_uniformly(3000)
        # self.scene_widgets[1].shape.geometries.reconstruct_mesh()

        Normalizer.normalize_shape(self.scene_widgets[1].shape)

        # Extract features and
        FeatureExtractor.extract_features(self.scene_widgets[1].shape)
        NormalizationFeatureExtractor.extract_normalization_features(self.scene_widgets[1].shape)
        self.features_widget_2.update_widget(self.scene_widgets[1].shape.features)
        self.normalization_widget.update_widget(self.scene_widgets[1].shape.normalization_features)
        self.scene_widgets[1].update_widget()

        # normalize_shape(self.scene_widgets[1].shape)
        # self.scene_widgets[1].shape = shape
        # self.scene_widgets[1].vis.update_geometry(self.scene_widgets[1].shape.geometries.mesh)

    def save_shape(self, file_path: str):
        self.scene_widgets[1].shape.save(file_path)

    def export_image_action(self, file_path: str):
        self.scene_widgets[1].vis.capture_screen_image(file_path)

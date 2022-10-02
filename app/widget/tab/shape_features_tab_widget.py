from copy import deepcopy

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout
from PyQt6.QtGui import QWindow

from app.widget.normalization_features_widget import NormalizationFeaturesWidget
from app.widget.util import color_widget
from app.widget.settings_widget import SettingsWidget
from app.widget.visualization_widget import VisualizationWidget

from src.object.settings import Settings
from app.util.os import IsMacOS
from src.pipeline.feature_extractor.normalization_feature_extractor import NormalizationFeatureExtractor


class ShapeFeaturesTabWidget(QWidget):
    def __init__(self):
        super(ShapeFeaturesTabWidget, self).__init__()
        color_widget(self, [0, 255, 0])

        # Left panel
        self.settings: Settings = Settings()
        self.settings_widget = SettingsWidget(self.settings)
        self.normalization_widget = NormalizationFeaturesWidget()

        # Widget 1
        self.scene_widget_1 = VisualizationWidget(self.settings, mesh_mode=True)
        if not IsMacOS:
            window_1 = QWindow.fromWinId(self.scene_widget_1.hwnd)
            window_container_1 = self.createWindowContainer(window_1, self.scene_widget_1)

        # Widget 2
        self.scene_widget_2 = VisualizationWidget(self.settings, convex_hull_mode=True)
        if not IsMacOS:
            window_2 = QWindow.fromWinId(self.scene_widget_2.hwnd)
            window_container_2 = self.createWindowContainer(window_2, self.scene_widget_2)

        # Widget 3
        self.scene_widget_3 = VisualizationWidget(self.settings, silhouette_mode=True)
        if not IsMacOS:
            window_3 = QWindow.fromWinId(self.scene_widget_3.hwnd)
            window_container_3 = self.createWindowContainer(window_3, self.scene_widget_3)

        # Connect the settings to the widget
        self.scene_widgets = [self.scene_widget_1, self.scene_widget_2, self.scene_widget_3]
        self.settings_widget.connect_visualizers(self.scene_widgets)

        # Assign scene widget here since that covers entire gui
        top_layout = QHBoxLayout()
        top_layout.addWidget(self.settings_widget)
        if not IsMacOS:
            top_layout.addWidget(window_container_1)
            top_layout.addWidget(window_container_2)
            top_layout.addWidget(window_container_3)

        bottom_layout = QHBoxLayout()
        bottom_layout.addWidget(self.normalization_widget)

        layout = QVBoxLayout(self)
        layout.addLayout(top_layout)
        layout.addLayout(bottom_layout)
        self.setLayout(layout)

    def load_shape(self, file_path: str):
        # Load the shapes
        self.scene_widgets[0].load_shape(file_path)

        # Populate widget 2 with the shape
        self.scene_widgets[1].clear()
        self.scene_widgets[1].shape = deepcopy(self.scene_widgets[0].shape)
        self.scene_widgets[1].update_widget()

        # Populate widget 3
        self.scene_widgets[2].clear()
        self.scene_widgets[2].shape = deepcopy(self.scene_widgets[0].shape)
        self.scene_widgets[2].update_widget()

        # Update normalization
        NormalizationFeatureExtractor.extract_features(
            self.scene_widgets[0].shape.geometries.mesh,
            self.scene_widgets[0].shape.geometries.point_cloud,
            self.scene_widgets[0].shape.geometries.axis_aligned_bounding_box,
            self.scene_widgets[0].shape.features.normalization_features,
        )

        self.normalization_widget.update_widget(self.scene_widgets[0].shape.features.normalization_features)

    def save_shape(self, file_path: str):
        self.scene_widgets[1].shape.save(file_path)

    def export_image_action(self, file_path: str):
        self.scene_widgets[1].vis.capture_screen_image(file_path)

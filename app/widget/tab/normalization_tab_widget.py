from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout
from PyQt6.QtGui import QWindow

from app.widget.features.normalization_features_widget import NormalizationFeaturesWidget
from app.widget.util import color_widget
from app.widget.settings_widget import SettingsWidget
from app.widget.features.shape_features_widget import ShapeFeaturesWidget
from app.widget.visualization_widget import VisualizationWidget
from src.controller.geometries_controller import GeometriesController

from src.object.settings import Settings
from src.pipeline.feature_extractor.shape_feature_extractor import ShapeFeatureExtractor
from src.pipeline.normalization_pipeline import NormalizationPipeline


class NormalizationTabWidget(QWidget):
    def __init__(self):
        super(NormalizationTabWidget, self).__init__()
        color_widget(self, [0, 255, 0])

        self.pipeline = NormalizationPipeline()

        # Left panel
        self.settings: Settings = Settings()
        self.settings_widget = SettingsWidget(self.settings)
        self.features_widget_1 = ShapeFeaturesWidget()

        # Widget 1
        self.scene_widget_1 = VisualizationWidget(self.settings)
        window_1 = QWindow.fromWinId(self.scene_widget_1.hwnd)
        window_container_1 = self.createWindowContainer(window_1, self.scene_widget_1)

        # Widget 2
        self.scene_widget_2 = VisualizationWidget(self.settings)
        window_2 = QWindow.fromWinId(self.scene_widget_2.hwnd)
        window_container_2 = self.createWindowContainer(window_2, self.scene_widget_2)

        # Right panel
        self.normalization_widget = NormalizationFeaturesWidget()
        self.features_widget_2 = ShapeFeaturesWidget()

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

        layout.addWidget(window_container_1)
        layout.addWidget(window_container_2)

        layout.addLayout(right_layout)
        self.setLayout(layout)

    def load_shape_from_path(self, file_path: str):
        # Load meshes
        self.scene_widgets[0].load_shape_from_path(file_path)
        self.scene_widgets[1].shape = self.pipeline.normalize_shape(file_path)
        GeometriesController.calculate_all_from_mesh(self.scene_widgets[1].shape.geometries)
        self.scene_widgets[1].load_shape(self.scene_widgets[1].shape)
        self.scene_widgets[1].update_widget()

        # Extract features of first shape
        if self.pipeline.shape_features.__contains__(self.scene_widgets[0].shape.geometries.path):
            self.scene_widgets[0].shape.features = self.pipeline.shape_features[self.scene_widgets[0].shape.geometries.path]
        if self.pipeline.shape_features.__contains__(self.scene_widgets[1].shape.geometries.path):
            self.scene_widgets[1].shape.features = self.pipeline.shape_features[self.scene_widgets[1].shape.geometries.path]

        ShapeFeatureExtractor.extract_all_shape_features(self.scene_widgets[0].shape)
        ShapeFeatureExtractor.extract_all_shape_features(self.scene_widgets[1].shape)

        self.features_widget_1.update_widget(self.scene_widgets[0].shape.features)
        self.features_widget_1.update_widget(self.scene_widgets[0].shape.features)
        self.features_widget_2.update_widget(self.scene_widgets[1].shape.features)
        self.normalization_widget.update_widget(self.scene_widgets[1].shape.features.normalization_features)

    def save_shape(self, file_path: str):
        self.scene_widgets[1].shape.save_ply(file_path)

    def export_image_action(self, file_path: str):
        self.scene_widgets[1].vis.capture_screen_image(file_path)

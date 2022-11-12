from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout
from PyQt6.QtGui import QWindow

from app.widget.settings_widget import SettingsWidget
from app.widget.features.shape_features_widget import ShapeFeaturesWidget
from app.widget.visualization_widget import VisualizationWidget
from app.widget.util import color_widget

from database.reader import FeatureDatabaseReader
from src.object.settings import Settings
from src.pipeline.feature_extractor.shape_feature_extractor import ShapeFeatureExtractor
from src.util.configs import *


class ViewerWidget(QWidget):
    def __init__(self):
        super(ViewerWidget, self).__init__()
        color_widget(self, [0, 255, 0])

        # Load all shape features
        self.shape_features = FeatureDatabaseReader.read_features_paths([
            os.path.join(DATABASE_ORIGINAL_DIR, DATABASE_FEATURES_FILENAME),
            os.path.join(DATABASE_NORMALIZED_DIR, DATABASE_FEATURES_FILENAME)
        ])

        # Left panel
        self.settings: Settings = Settings()
        self.settings_widget = SettingsWidget(self.settings)
        self.features_widget = ShapeFeaturesWidget()

        self.visualization_widget = VisualizationWidget(self.settings)
        window = QWindow.fromWinId(self.visualization_widget.hwnd)
        window_container = self.createWindowContainer(window, self.visualization_widget)

        # Connect the settings to the widget
        self.scene_widgets = [self.visualization_widget]
        self.settings_widget.connect_visualizers(self.scene_widgets)

        # Set the layout of the widget
        left_layout = QVBoxLayout()
        left_layout.addWidget(self.settings_widget)
        left_layout.addWidget(self.features_widget)

        layout = QHBoxLayout(self)
        layout.addLayout(left_layout)
        layout.addWidget(window_container)
        self.setLayout(layout)

    def load_shape_from_path(self, file_path: str):
        self.scene_widgets[0].load_shape_from_path(file_path)
        if self.shape_features.__contains__(self.scene_widgets[0].shape.geometries.path):
            self.scene_widgets[0].shape.features = self.shape_features[self.scene_widgets[0].shape.geometries.path]

        ShapeFeatureExtractor.extract_all_shape_features(self.scene_widgets[0].shape)
        self.features_widget.update_widget(self.scene_widgets[0].shape.features)

    def save_shape(self, file_path: str):
        self.scene_widgets[0].shape.save_ply(file_path)

    def export_image_action(self, file_path: str):
        self.scene_widgets[0].vis.capture_screen_image(file_path)

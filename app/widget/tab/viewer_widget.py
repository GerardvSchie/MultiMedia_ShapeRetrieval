from app.widget.settings_widget import SettingsWidget
from app.widget.features.shape_features_widget import ShapeFeaturesWidget
from app.widget.visualization_widget import VisualizationWidget
from app.widget.util import color_widget

from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout
from PyQt6.QtGui import QWindow


from src.object.settings import Settings
from app.util.os import IsMacOS
from src.pipeline.feature_extractor.shape_feature_extractor import ShapeFeatureExtractor


class ViewerWidget(QWidget):
    def __init__(self):
        super(ViewerWidget, self).__init__()
        color_widget(self, [0, 255, 0])

        # Left panel
        self.settings: Settings = Settings()
        self.settings_widget = SettingsWidget(self.settings)
        self.features_widget = ShapeFeaturesWidget()

        self.visualization_widget = VisualizationWidget(self.settings)
        if not IsMacOS:
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
        if not IsMacOS:
            layout.addWidget(window_container)
        self.setLayout(layout)

    def load_shape(self, file_path: str):
        self.scene_widgets[0].load_shape(file_path)
        ShapeFeatureExtractor.extract_all_shape_features(self.scene_widgets[0].shape)
        self.features_widget.update_widget(self.scene_widgets[0].shape.features)

    def save_shape(self, file_path: str):
        self.scene_widgets[0].shape.save(file_path)

    def export_image_action(self, file_path: str):
        self.scene_widgets[0].vis.capture_screen_image(file_path)

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton
from PyQt6.QtGui import QWindow

from app.widget.util import color_widget
from app.widget.settings_widget import SettingsWidget
from app.widget.features_widget import FeaturesWidget
from app.widget.visualization_widget import VisualizationWidget

from src.object.settings import Settings
from app.util.os import IsMacOS
from src.pipeline.normalization import normalize_shape


class NormalizationTabWidget(QWidget):
    def __init__(self, settings: Settings):
        super(NormalizationTabWidget, self).__init__()
        color_widget(self, [0, 255, 0])

        # Left panel
        settings_widget = SettingsWidget(settings)
        features_widget = FeaturesWidget()

        # Widget 1
        scene_widget_1 = VisualizationWidget(settings)
        if not IsMacOS:
            window_1 = QWindow.fromWinId(scene_widget_1.hwnd)
            window_container_1 = self.createWindowContainer(window_1, scene_widget_1)

        # Widget 2
        scene_widget_2 = VisualizationWidget(settings)
        if not IsMacOS:
            window_2 = QWindow.fromWinId(scene_widget_2.hwnd)
            window_container_2 = self.createWindowContainer(window_2, scene_widget_2)

        # Connect the settings to the widget
        scene_widget_1.connect_features(features_widget)
        self.scene_widgets = [scene_widget_1, scene_widget_2]
        settings_widget.connect_visualizers(self.scene_widgets)

        # Assign scene widget here since that covers entire gui
        layout = QHBoxLayout(self)

        left_layout = QVBoxLayout()
        left_layout.addWidget(settings_widget)
        left_layout.addWidget(features_widget)
        layout.addLayout(left_layout)

        if not IsMacOS:
            layout.addWidget(window_container_1)
            layout.addWidget(window_container_2)
        self.setLayout(layout)

    def load_shape(self, file_path: str):
        # Original mesh
        self.scene_widgets[0].load_shape(file_path)

        # Normalized mesh with less points
        self.scene_widgets[1].load_shape(file_path)
        shape = self.scene_widgets[1].shape

        self.scene_widgets[1].vis.clear_geometries()
        self.scene_widgets[1].clear_geometries_state()

        shape.geometries.point_cloud = shape.geometries.mesh.sample_points_poisson_disk(3000)
        # shape.geometries.point_cloud = shape.geometries.mesh.sample_points_uniformly(3000)
        shape.geometries.reconstruct_mesh()

        # normalize_shape(self.scene_widgets[1].shape)
        # self.scene_widgets[1].vis.update_geometry(self.scene_widgets[1].shape.geometries.mesh)

    def save_shape(self, file_path: str):
        self.scene_widgets[1].shape.save(file_path)

    def export_image_action(self, file_path: str):
        self.scene_widgets[1].vis.capture_screen_image(file_path)

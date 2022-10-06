from copy import deepcopy

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout
from PyQt6.QtGui import QWindow

from app.widget.features.normalization_features_widget import NormalizationFeaturesWidget
from app.widget.util import color_widget
from app.widget.settings_widget import SettingsWidget
from app.widget.features.shape_features_widget import ShapeFeaturesWidget
from app.widget.visualization_widget import VisualizationWidget

from src.object.settings import Settings
from app.util.os import IsMacOS
from src.pipeline.feature_extractor.shape_feature_extractor import ShapeFeatureExtractor
from src.pipeline.normalization import Normalizer
from src.controller.geometries_controller import GeometriesController


class NormalizationTabWidget(QWidget):
    def __init__(self):
        super(NormalizationTabWidget, self).__init__()
        color_widget(self, [0, 255, 0])

        # Left panel
        self.settings: Settings = Settings()
        self.settings_widget = SettingsWidget(self.settings)
        self.features_widget_1 = ShapeFeaturesWidget()

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

        if not IsMacOS:
            layout.addWidget(window_container_1)
            layout.addWidget(window_container_2)

        layout.addLayout(right_layout)
        self.setLayout(layout)

    def load_shape(self, file_path: str):
        # Load meshes
        self.scene_widgets[0].load_shape(file_path)
        self.scene_widgets[1].clear()
        self.scene_widgets[1].shape = deepcopy(self.scene_widgets[0].shape)

        # Extract features of first shape
        ShapeFeatureExtractor.extract_all_shape_features(self.scene_widgets[0].shape)
        self.features_widget_1.update_widget(self.scene_widgets[0].shape.features)

        # Normalized mesh with 3000 points
        # self.scene_widgets[1].shape.geometries.point_cloud = self.scene_widgets[1].shape.geometries.mesh.sample_points_poisson_disk(3000)
        # self.scene_widgets[1].shape.geometries.point_cloud = self.scene_widgets[1].shape.geometries.mesh.sample_points_uniformly(3000)
        #
        # GeometriesController.calculate_all_from_point_cloud(self.scene_widgets[1].shape.geometries, True)
        # GeometriesController.calculate_mesh_normals(self.scene_widgets[1].shape.geometries, True)
        # GeometriesController.calculate_point_cloud_normals(self.scene_widgets[1].shape.geometries, True)

        Normalizer.normalize_shape(self.scene_widgets[1].shape)

        # Reconstruct all things of the mesh
        GeometriesController.calculate_all_from_mesh(self.scene_widgets[1].shape.geometries, True)
        GeometriesController.calculate_point_cloud_normals(self.scene_widgets[1].shape.geometries, True)
        GeometriesController.calculate_mesh_normals(self.scene_widgets[1].shape.geometries, True)
        GeometriesController.calculate_gui_geometries(self.scene_widgets[1].shape.geometries, True)

        # Extract features and update the panels
        ShapeFeatureExtractor.extract_all_shape_features(self.scene_widgets[1].shape)
        self.features_widget_2.update_widget(self.scene_widgets[1].shape.features)
        self.normalization_widget.update_widget(self.scene_widgets[1].shape.features.normalization_features)

        self.scene_widgets[1].update_widget()

    def save_shape(self, file_path: str):
        self.scene_widgets[1].shape.save(file_path)

    def export_image_action(self, file_path: str):
        self.scene_widgets[1].vis.capture_screen_image(file_path)

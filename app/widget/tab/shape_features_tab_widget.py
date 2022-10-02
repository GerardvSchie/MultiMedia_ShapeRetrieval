from copy import deepcopy
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QWindow

from app.widget.features.mesh_features_widget import MeshFeaturesWidget
from app.widget.features.silhouette_features_widget import SilhouetteFeaturesWidget
from src.object.settings import Settings
from src.pipeline.feature_extractor.normalization_feature_extractor import NormalizationFeatureExtractor

from app.util.font import BOLD_FONT
from app.util.os import IsMacOS
from app.widget.features.normalization_features_widget import NormalizationFeaturesWidget
from app.widget.util import color_widget
from app.widget.settings_widget import SettingsWidget
from app.widget.visualization_widget import VisualizationWidget
from src.pipeline.feature_extractor.shape_feature_extractor import ShapeFeatureExtractor
from src.pipeline.feature_extractor.silhouette_feature_extractor import SilhouetteFeatureExtractor


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
        left_layout = QVBoxLayout()
        left_layout.addWidget(self.settings_widget)
        left_layout.addWidget(self.normalization_widget)

        mesh_layout = QVBoxLayout()
        mesh_layout.addWidget(ShapeFeaturesTabWidget._create_header("Mesh View"))
        if not IsMacOS:
            mesh_layout.addWidget(window_container_1)
        self.mesh_features_widget = MeshFeaturesWidget()
        mesh_layout.addWidget(self.mesh_features_widget)

        convex_hull_layout = QVBoxLayout()
        convex_hull_layout.addWidget(ShapeFeaturesTabWidget._create_header("Convex Hull View"))
        if not IsMacOS:
            convex_hull_layout.addWidget(window_container_2)
        self.convex_hull_features_widget = MeshFeaturesWidget()
        convex_hull_layout.addWidget(self.convex_hull_features_widget)

        silhouette_layout = QVBoxLayout()
        silhouette_layout.addWidget(ShapeFeaturesTabWidget._create_header("Silhouette View"))
        if not IsMacOS:
            silhouette_layout.addWidget(window_container_3)
        self.silhouette_features_widget = SilhouetteFeaturesWidget()
        silhouette_layout.addWidget(self.silhouette_features_widget)

        layout = QHBoxLayout(self)
        layout.addLayout(left_layout)
        layout.addLayout(mesh_layout)
        layout.addLayout(convex_hull_layout)
        layout.addLayout(silhouette_layout)
        self.setLayout(layout)

    @staticmethod
    def _create_header(text: str) -> QLabel:
        header_label = QLabel(text)
        header_label.setFont(BOLD_FONT)
        header_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_label.setMaximumHeight(20)
        return header_label

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
        self.scene_widgets[2].update_vis()

        # Save silhouette to file
        self.scene_widgets[2].vis.capture_screen_image("data/temp.png")

        ShapeFeatureExtractor.extract_all_shape_features(self.scene_widgets[0].shape)
        self.normalization_widget.update_widget(self.scene_widgets[0].shape.features.normalization_features)
        self.mesh_features_widget.update_widget(self.scene_widgets[0].shape.features.mesh_features)
        self.convex_hull_features_widget.update_widget(self.scene_widgets[0].shape.features.convex_hull_features)

        SilhouetteFeatureExtractor.extract_features("data/temp.png", self.scene_widgets[0].shape.features.silhouette_features)
        self.silhouette_features_widget.update_widget(self.scene_widgets[0].shape.features.silhouette_features)



        # # Update normalization
        # NormalizationFeatureExtractor.extract_features(
        #     self.scene_widgets[0].shape.geometries.mesh,
        #     self.scene_widgets[0].shape.geometries.point_cloud,
        #     self.scene_widgets[0].shape.geometries.axis_aligned_bounding_box,
        #     self.scene_widgets[0].shape.features.normalization_features,
        # )

    def save_shape(self, file_path: str):
        self.scene_widgets[1].shape.save(file_path)

    def export_image_action(self, file_path: str):
        self.scene_widgets[1].vis.capture_screen_image(file_path)

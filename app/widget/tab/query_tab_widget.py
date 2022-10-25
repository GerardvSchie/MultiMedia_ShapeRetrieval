import os
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QGridLayout
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QWindow

from src.database.querier import DatabaseQuerier
from src.object.features.shape_features import ShapeFeatures
from src.object.settings import Settings
from src.util.configs import *

from app.util.font import BOLD_FONT
from app.widget.util import color_widget
from app.widget.settings_widget import SettingsWidget
from app.widget.visualization_widget import VisualizationWidget
from src.pipeline.feature_extractor.shape_feature_extractor import ShapeFeatureExtractor


class QueryTabWidget(QWidget):
    def __init__(self):
        super(QueryTabWidget, self).__init__()
        color_widget(self, [0, 255, 0])

        # Left panel
        self.settings: Settings = Settings()
        self.settings_widget = SettingsWidget(self.settings)

        # Load widget
        self.scene_widget_0 = VisualizationWidget(self.settings)
        window_0 = QWindow.fromWinId(self.scene_widget_0.hwnd)
        window_container_0 = self.createWindowContainer(window_0, self.scene_widget_0)

        # Widget 1
        self.scene_widget_1 = VisualizationWidget(self.settings)
        window_1 = QWindow.fromWinId(self.scene_widget_1.hwnd)
        window_container_1 = self.createWindowContainer(window_1, self.scene_widget_1)

        # Widget 2
        self.scene_widget_2 = VisualizationWidget(self.settings)
        window_2 = QWindow.fromWinId(self.scene_widget_2.hwnd)
        window_container_2 = self.createWindowContainer(window_2, self.scene_widget_2)

        # Widget 3
        self.scene_widget_3 = VisualizationWidget(self.settings)
        window_3 = QWindow.fromWinId(self.scene_widget_3.hwnd)
        window_container_3 = self.createWindowContainer(window_3, self.scene_widget_3)

        self.querier = DatabaseQuerier(os.path.join(DATABASE_REFINED_DIR, DATABASE_NORMALIZED_DESCRIPTORS_FILENAME))

        # Connect the settings to the widget
        self.scene_widgets = [self.scene_widget_0, self.scene_widget_1, self.scene_widget_2, self.scene_widget_3]
        self.settings_widget.connect_visualizers(self.scene_widgets)

        # Assign scene widget here since that covers entire gui
        left_layout = QVBoxLayout()
        left_layout.addWidget(QueryTabWidget._create_header("Query shape"))
        left_layout.addWidget(window_container_0)
        left_layout.addWidget(self.settings_widget)

        grid_layout = QGridLayout()
        grid_layout.addWidget(QueryTabWidget._create_header("Result 1"), 0, 0, 1, 1)
        grid_layout.addWidget(QueryTabWidget._create_header("Result 2"), 0, 1, 1, 1)
        grid_layout.addWidget(QueryTabWidget._create_header("Result 3"), 0, 2, 1, 1)

        grid_layout.addWidget(window_container_1, 1, 0, 1, 1)
        grid_layout.addWidget(window_container_2, 1, 1, 1, 1)
        grid_layout.addWidget(window_container_3, 1, 2, 1, 1)

        layout = QHBoxLayout(self)
        layout.addLayout(left_layout)
        layout.addLayout(grid_layout)
        self.setLayout(layout)

    @staticmethod
    def _create_header(text: str) -> QLabel:
        header_label = QLabel(text)
        header_label.setFont(BOLD_FONT)
        header_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_label.setMaximumHeight(20)
        return header_label

    def load_shape_from_path(self, file_path: str):
        # Load the shapes
        self.scene_widget_0.load_shape_from_path(file_path)

        # Query
        queried_shape_paths = []
        ShapeFeatureExtractor.extract_all_shape_features(self.scene_widgets[0].shape)

        # Populate widget 1 with the shape
        self.scene_widget_1.clear()
        # self.scene_widget_1.load_shape(queried_shape_paths[0])
        self.scene_widget_1.update_widget()

        # Populate widget 2 with the shape
        self.scene_widget_2.clear()
        # self.scene_widget_2.load_shape(queried_shape_paths[1])
        self.scene_widget_2.update_widget()

        # Populate widget 3 with the shape
        self.scene_widget_3.clear()
        # self.scene_widget_3.load_shape(queried_shape_paths[2])
        self.scene_widget_3.update_widget()

    def save_shape(self, file_path: str):
        pass
        # self.scene_widgets[1].shape.save_ply(file_path)

    def export_image_action(self, file_path: str):
        self.scene_widget_0.vis.capture_screen_image(file_path)

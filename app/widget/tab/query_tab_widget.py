from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QGridLayout
from PyQt6.QtGui import QWindow

from app.widget.query_result_widget import QueryResultWidget
from src.database.querier import CustomFeatureDatabaseQuerier
from src.object.settings import Settings

from app.widget.util import color_widget, create_header_label
from app.widget.settings_widget import SettingsWidget
from app.widget.visualization_widget import VisualizationWidget
from src.pipeline.compute_descriptors import compute_descriptors
from src.pipeline.feature_extractor.shape_feature_extractor import ShapeFeatureExtractor
from src.pipeline.normalization_pipeline import NormalizationPipeline
from src.util.configs import *


class QueryTabWidget(QWidget):
    RESULTS_PER_ROW = 5

    def __init__(self):
        super(QueryTabWidget, self).__init__()
        color_widget(self, [0, 255, 0])

        # Left panel
        self.settings: Settings = Settings()
        self.settings_widget = SettingsWidget(self.settings)
        self.pipeline = NormalizationPipeline()
        # self.querier = DatabaseQuerier(os.path.join(DATABASE_REFINED_DIR, DATABASE_NORMALIZED_DESCRIPTORS_FILENAME))
        self.querier = CustomFeatureDatabaseQuerier(os.path.join(DATABASE_NORMALIZED_DIR, DATABASE_NORMALIZED_DESCRIPTORS_FILENAME))

        # Load widget
        self.query_scene_widget = VisualizationWidget(self.settings)
        window = QWindow.fromWinId(self.query_scene_widget.hwnd)
        window_container = self.createWindowContainer(window, self.query_scene_widget)

        self.query_result_widgets: [QueryResultWidget] = []

        grid_layout = QGridLayout()
        for i in range(NR_RESULTS):
            query_widget = QueryResultWidget(f'Result {i+1}', self.settings)
            self.query_result_widgets.append(query_widget)
            grid_layout.addWidget(query_widget, int(i / QueryTabWidget.RESULTS_PER_ROW), i % QueryTabWidget.RESULTS_PER_ROW, 1, 1)

        # Connect the settings to the widget
        self.scene_widgets = [self.query_scene_widget] + [widget.scene_widget for widget in self.query_result_widgets]
        self.settings_widget.connect_visualizers(self.scene_widgets)

        # Assign scene widget here since that covers entire gui
        left_layout = QVBoxLayout()
        left_layout.addWidget(create_header_label("Query shape"))
        left_layout.addWidget(window_container)
        left_layout.addWidget(self.settings_widget)

        layout = QHBoxLayout(self)
        layout.addLayout(left_layout)
        layout.addLayout(grid_layout)
        self.setLayout(layout)

    def load_shape_from_path(self, file_path: str):
        # Load the shapes
        self.query_scene_widget.load_shape_from_path(file_path)
        normalized_shape = self.pipeline.normalize_shape(file_path)
        ShapeFeatureExtractor.extract_all_shape_features(normalized_shape)
        compute_descriptors(normalized_shape)

        queried_shape_paths, distances = self.querier.query_descriptor(normalized_shape.descriptors)
        # Dummy query
        # queried_shape_paths, distances = ['data\\LabeledDB_new\\Airplane\\61\\refined.ply'] * QueryTabWidget.NR_RESULTS, range(1, 100)

        for query_index in range(len(self.query_result_widgets)):
            query_result_widget = self.query_result_widgets[query_index]
            query_result_widget.load_shape_from_path(queried_shape_paths[query_index], distances[query_index])

    def save_shape(self, file_path: str):
        pass

    def export_image_action(self, file_path: str):
        self.query_scene_widget.vis.capture_screen_image(file_path)

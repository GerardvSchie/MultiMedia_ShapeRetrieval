from PyQt6.QtWidgets import QWidget, QHBoxLayout

from app.widget.table_widget import TableWidget
from app.widget.util import color_widget
from database.features.reader import FeatureDatabaseReader
from database.features.writer import FeatureDatabaseWriter
from src.object.shape import Shape
from src.util.configs import *


class FeaturesTableTabWidget(QWidget):
    def __init__(self):
        super(FeaturesTableTabWidget, self).__init__()
        color_widget(self, [0, 255, 0])

        shape_features = FeatureDatabaseReader.read_features(os.path.join(DATABASE_NORMALIZED_DIR, DATABASE_FEATURES_FILENAME))
        shape_list = []

        for identifier in shape_features:
            shape = Shape(identifier)
            shape.features = shape_features[identifier]
            shape_list.append(shape)

        table_widget = TableWidget(shape_list, FeatureDatabaseWriter.get_features_list, FeatureDatabaseWriter.FEATURES_HEADER)

        layout = QHBoxLayout()
        layout.addWidget(table_widget)
        self.setLayout(layout)

        self.scene_widgets = []

    def load_shape_from_path(self, file_path: str):
        pass

    def save_shape(self, file_path: str):
        pass

    def export_image_action(self, file_path: str):
        pass

from PyQt6.QtWidgets import QWidget, QHBoxLayout

from app.widget.table_widget import TableWidget
from app.widget.util import color_widget
from src.database.reader import DatabaseReader
from src.database.writer import DatabaseWriter
from src.object.shape import Shape


class FeaturesTableTabWidget(QWidget):
    def __init__(self):
        super(FeaturesTableTabWidget, self).__init__()
        color_widget(self, [0, 255, 0])

        shape_features = DatabaseReader.read_features('data/database/original_features.csv')
        shape_list = []

        for identifier in shape_features:
            shape = Shape(identifier)
            shape.features = shape_features[identifier]
            shape_list.append(shape)

        table_widget = TableWidget(shape_list, DatabaseWriter.get_features_list, DatabaseWriter.FEATURES_HEADER)

        layout = QHBoxLayout()
        layout.addWidget(table_widget)
        self.setLayout(layout)

        self.scene_widgets = []

    def load_shape(self, file_path: str):
        pass

    def save_shape(self, file_path: str):
        pass

    def export_image_action(self, file_path: str):
        pass

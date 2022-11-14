from PyQt6.QtWidgets import QWidget, QHBoxLayout

from app.widget.table_widget import TableWidget
from app.widget.util import color_widget
from src.database.reader import FeatureDatabaseReader
from src.database.writer import FeatureDatabaseWriter
from src.object.shape import Shape
from src.util.configs import *


class NormalizedDescriptorsTableTabWidget(QWidget):
    def __init__(self):
        super(NormalizedDescriptorsTableTabWidget, self).__init__()
        color_widget(self, [0, 255, 0])

        shape_descriptors = FeatureDatabaseReader.read_descriptors(os.path.join(DATABASE_NORMALIZED_DIR, DATABASE_NORMALIZED_DESCRIPTORS_FILENAME))
        shape_list = []

        for identifier in shape_descriptors:
            shape = Shape(identifier)
            shape.descriptors = shape_descriptors[identifier]
            shape_list.append(shape)

        table_widget = TableWidget(shape_list, FeatureDatabaseWriter.get_descriptors_list, FeatureDatabaseWriter.DESCRIPTORS_HEADER)

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

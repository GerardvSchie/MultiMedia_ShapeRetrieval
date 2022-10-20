from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout

from app.widget.table_widget import TableWidget
from app.widget.util import color_widget
from src.object.features.shape_features import ShapeFeatures


class DatabaseTabWidget(QWidget):
    def __init__(self):
        super(DatabaseTabWidget, self).__init__()
        color_widget(self, [0, 255, 0])

        table_widget = TableWidget()

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

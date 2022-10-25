from PyQt6.QtWidgets import QWidget, QVBoxLayout
from PyQt6.QtGui import QWindow

from app.widget.descriptors_widget import DescriptorsWidget
from app.widget.util import color_widget, create_header_label
from app.widget.visualization_widget import VisualizationWidget
from src.object.descriptors import Descriptors


class QueryResultWidget(QWidget):
    def __init__(self, title, settings):
        super(QueryResultWidget, self).__init__()
        color_widget(self, [255, 122, 122])

        self.settings = settings

        # Load widget
        self.scene_widget = VisualizationWidget(self.settings)
        self.descriptor_widget = DescriptorsWidget()
        self.distance_label = create_header_label("-")

        # Capture scene widget into a window
        window = QWindow.fromWinId(self.scene_widget.hwnd)
        window_container = self.createWindowContainer(window, self.scene_widget)

        # Assign scene widget here since that covers entire gui
        layout = QVBoxLayout()
        layout.addWidget(create_header_label(title))
        layout.addWidget(window_container)
        layout.addWidget(self.distance_label)
        layout.addWidget(self.descriptor_widget)
        self.setLayout(layout)

    def load_shape_from_path(self, file_path: str, distance: float, shape_descriptors: Descriptors):
        self.scene_widget.clear()
        self.scene_widget.load_shape_from_path(file_path)
        self.scene_widget.update_widget()
        self.distance_label.setText(str(distance))
        self.descriptor_widget.update_widget(shape_descriptors)

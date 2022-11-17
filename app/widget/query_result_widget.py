from PyQt6.QtWidgets import QWidget, QVBoxLayout
from PyQt6.QtGui import QWindow

from app.widget.util import color_widget, create_header_label
from app.widget.visualization_widget import VisualizationWidget


class QueryResultWidget(QWidget):
    def __init__(self, title, settings):
        super(QueryResultWidget, self).__init__()
        color_widget(self, [255, 122, 122])

        self.settings = settings

        # Load widget
        self.scene_widget = VisualizationWidget(self.settings)
        self.distance_label = create_header_label("Distance: -")

        # Capture scene widget into a window
        window = QWindow.fromWinId(self.scene_widget.hwnd)
        window_container = self.createWindowContainer(window, self.scene_widget)

        # Assign scene widget here since that covers entire gui
        layout = QVBoxLayout()
        layout.addWidget(create_header_label(title))
        layout.addWidget(window_container)
        layout.addWidget(self.distance_label)
        self.setLayout(layout)

    def load_shape_from_path(self, file_path: str, distance: float):
        self.scene_widget.clear()
        self.scene_widget.load_shape_from_path(file_path)
        self.scene_widget.update_widget()
        self.distance_label.setText(f"Distance: {distance:.5f}")

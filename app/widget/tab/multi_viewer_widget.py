from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton
from PyQt6.QtGui import QWindow

from app.widget.util import color_widget
from app.widget.visualization_widget import VisualizationWidget

from src.object.settings import Settings
from app.util.os import IsMacOS


class MultiViewerWidget(QWidget):
    def __init__(self, settings: Settings):
        super(MultiViewerWidget, self).__init__()
        color_widget(self, [0, 255, 0])

        # Widget 1
        scene_widget_1 = VisualizationWidget(settings)
        if not IsMacOS:
            window_1 = QWindow.fromWinId(scene_widget_1.hwnd)
            window_container_1 = self.createWindowContainer(window_1, scene_widget_1)

        # Widget 2
        scene_widget_2 = VisualizationWidget(settings)
        if not IsMacOS:
            window_2 = QWindow.fromWinId(scene_widget_2.hwnd)
            window_container_2 = self.createWindowContainer(window_2, scene_widget_2)

        btn = QPushButton(text="test")
        btn.clicked.connect(lambda: print("Button pressed!"))

        # Assign scene widget here since that covers entire gui
        layout = QVBoxLayout(self)
        if not IsMacOS:
            layout.addWidget(window_container_1)
            layout.addWidget(window_container_2)
        layout.addWidget(btn)
        self.setLayout(layout)

        self.scene_widgets = [scene_widget_1, scene_widget_2]

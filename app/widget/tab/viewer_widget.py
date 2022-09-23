from app.widget.settings_widget import SettingsWidget
from app.widget.util import color_widget

from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout
from PyQt6.QtGui import QWindow

from app.widget.features_widget import FeaturesWidget
from app.widget.visualization_widget import VisualizationWidget

from src.object.settings import Settings


class ViewerWidget(QWidget):
    def __init__(self, settings: Settings):
        super(ViewerWidget, self).__init__()
        color_widget(self, [0, 255, 0])

        settings_widget = SettingsWidget(settings)
        settings_widget.setFixedWidth(150)
        features_widget = FeaturesWidget()
        features_widget.setFixedWidth(150)

        visualization_widget = VisualizationWidget(settings)
        window = QWindow.fromWinId(visualization_widget.hwnd)
        window_container = self.createWindowContainer(window, visualization_widget)

        # Connect the settings to the widget
        settings_widget.connect_visualizer(visualization_widget)
        visualization_widget.connect_features(features_widget)
        self.scene_widgets = [visualization_widget]

        # Set the layout of the widget
        layout = QHBoxLayout(self)

        left_layout = QVBoxLayout()
        left_layout.addWidget(settings_widget)
        left_layout.addWidget(features_widget)

        layout.addLayout(left_layout)
        layout.addWidget(window_container)
        self.setLayout(layout)

    # def __init__(self, settings: Settings):
    #     super(ViewerWidget, self).__init__()
    #     settings_widget = SettingsWidget(settings)
    #     settings_widget.setFixedWidth(150)
    #     features_widget = FeaturesWidget()
    #     features_widget.setFixedWidth(150)
    #
    #     scene_window = VisualizationWindow(settings)
    #     window_container = self.createWindowContainer(scene_window, self)
    #     # scene_widget = VisualizationWidget(self.settings)
    #     # window = QtGui.QWindow.fromWinId(scene_widget.hwnd)
    #     # window_container = self.createWindowContainer(window, scene_widget)
    #
    #     color_widget(settings_widget, [0, 255, 255])
    #     color_widget(features_widget, [255, 255, 0])
    #
    #     # Connect the settings to the widget
    #     settings_widget.connect_visualizer(scene_window.visualization_widget)
    #     features_widget.connect_visualizer(scene_window.visualization_widget)
    #     self.scene_widgets = [scene_window.visualization_widget]
    #
    #     # Set the layout of the widget
    #     layout = QHBoxLayout(self)
    #
    #     left_layout = QVBoxLayout()
    #     left_layout.addWidget(settings_widget)
    #     left_layout.addWidget(features_widget)
    #
    #     layout.addLayout(left_layout)
    #     layout.addWidget(window_container)
    #     self.setLayout(layout)
    #

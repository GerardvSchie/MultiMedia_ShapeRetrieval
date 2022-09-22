import logging

from app.widget.visualization_widget import VisualizationWidget
from src.object.features import Features

from PyQt6 import QtWidgets, QtGui, QtCore
from PyQt6.QtWidgets import QTabWidget, QGridLayout, QWidget, QVBoxLayout, QComboBox, QLabel, QColorDialog
from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtWidgets import QMainWindow, QApplication


class FeaturesWidget(QWidget):
    def __init__(self):
        super(FeaturesWidget, self).__init__()
        # Widget state of main app window and the scene that is controlled by the settings
        self.visualization_widget = None

        # Widget
        # Render mode combobox
        render_mode_combobox = QLabel("Class")

        # Create layout
        layout = QGridLayout()
        layout.addWidget(render_mode_combobox)
        self.setLayout(layout)

    def connect_visualizer(self, visualization_widget: VisualizationWidget):
        self.visualization_widget = visualization_widget



import logging
from app.widget.settings_widget import SettingsWidget

from PyQt6 import QtWidgets, QtGui, QtCore, QtQuickWidgets, QtQuick
from PyQt6.QtWidgets import QTabWidget, QGridLayout, QWidget

from app.util.worker import Worker
from app.widget.visualization_widget import VisualizationWidget
from app.widget.features_widget import FeaturesWidget
from app.gui.menu_bar import MenuBar
from src.object.settings import Settings
from PyQt6.QtGui import QAction, QIcon, QPalette, QColor
from PyQt6.QtWidgets import QMainWindow, QApplication


def color_widget(widget: QWidget, rgb: [int]):
    widget.setAutoFillBackground(True)
    widget.setPalette(QPalette(QColor(rgb[0], rgb[1], rgb[2])))

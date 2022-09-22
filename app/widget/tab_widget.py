import logging
from app.widget.settings_widget import SettingsWidget
from app.util.widget import color_widget

from PyQt6 import QtWidgets, QtGui, QtCore, QtQuickWidgets, QtQuick
from PyQt6.QtWidgets import QTabWidget, QGridLayout, QWidget

from app.util.worker import Worker
from app.widget.visualization_widget import VisualizationWidget
from app.widget.features_widget import FeaturesWidget
from app.gui.menu_bar import MenuBar
from src.object.settings import Settings
from PyQt6.QtGui import QAction, QIcon, QPalette, QColor
from PyQt6.QtWidgets import QMainWindow, QApplication


class TabWidget(QTabWidget):
    def __init__(self):
        super(TabWidget, self).__init__()

        # Central settings for the tabs
        self.settings = Settings()

        # Start thread that handles the events on o3d windows
        self.thread = QtCore.QThread()
        self.worker = Worker()
        self.thread.started.connect(lambda: self.worker.run())
        self.thread.start()

        self.currentChanged.connect(lambda index: self.custom_currentChanged(index))

        # Tab widget
        color_widget(self, [255, 0, 0])

        # Tab 1
        self.tab1_widgets = []
        self.tab1_widget = self.tab_1_widget()
        color_widget(self.tab1_widget, [0, 255, 0])
        self.addTab(self.tab1_widget, "Mesh inspect")

        # Tab 2
        self.tab2_widgets = []
        self.tab2_widget = self.tab_2_widget()
        color_widget(self.tab2_widget, [0, 255, 0])
        self.addTab(self.tab2_widget, "Mesh inspect 2")

        # Select tab 1
        self.tab_1_select()

    def custom_currentChanged(self, index: int):
        if index == 0:
            print("Changed to tab 1")
            self.tab_1_select()
            # self.tab1_widget.setVisible(True)
            # self.tab2_widget.setVisible(False)
            # self.setCurrentWidget(self.tab1_widget)
        if index == 1:
            print("Changed to tab 2")
            self.tab_2_select()
            # self.tab2_widget.setVisible(True)
            # self.tab1_widget.setVisible(False)
            # self.setCurrentWidget(self.tab2_widget)

        # Try update the widget
        self.update()

    def tab_1_widget(self) -> QWidget:
        settings_widget = SettingsWidget(self.settings)
        color_widget(settings_widget, [0, 0, 255])
        settings_widget.setFixedWidth(150)
        features_widget = FeaturesWidget()
        features_widget.setFixedWidth(150)

        scene_widget = VisualizationWidget(self.settings)
        window = QtGui.QWindow.fromWinId(scene_widget.hwnd)
        window_container = self.createWindowContainer(window, scene_widget)

        color_widget(settings_widget, [0, 255, 255])
        color_widget(features_widget, [255, 255, 0])

        # Connect the settings to the widget
        settings_widget.connect_visualizer(scene_widget)
        features_widget.connect_visualizer(scene_widget)

        # Assign scene widget here since that covers entire gui
        widget = QWidget()
        layout = QtWidgets.QHBoxLayout(self)

        left_layout = QtWidgets.QVBoxLayout()
        left_layout.addWidget(settings_widget)
        left_layout.addWidget(features_widget)

        layout.addLayout(left_layout)
        layout.addWidget(window_container)
        widget.setLayout(layout)

        self.tab1_widgets = [scene_widget]
        return widget

    def tab_2_widget(self) -> QWidget:
        # Widget 1
        scene_widget_1 = VisualizationWidget(self.settings)
        window_1 = QtGui.QWindow.fromWinId(scene_widget_1.hwnd)
        window_container_1 = self.createWindowContainer(window_1, scene_widget_1)

        # Widget 2
        scene_widget_2 = VisualizationWidget(self.settings)
        window_2 = QtGui.QWindow.fromWinId(scene_widget_2.hwnd)
        window_container_2 = self.createWindowContainer(window_2, scene_widget_2)

        btn = QtWidgets.QPushButton(text="test")
        btn.clicked.connect(lambda: print("Button pressed!"))

        # Assign scene widget here since that covers entire gui
        widget = QWidget()
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(window_container_1)
        layout.addWidget(window_container_2)
        layout.addWidget(btn)
        widget.setLayout(layout)

        self.tab2_widgets = [scene_widget_1, scene_widget_2]
        return widget

    def tab_1_select(self):
        self.worker.set_scenes([self.tab1_widgets[0]])
        TabWidget.connect_to_menu_bar(self.tab1_widgets[0], self.tab1_widgets[0])

    def tab_2_select(self):
        self.worker.set_scenes([self.tab2_widgets[0], self.tab2_widgets[1]])
        TabWidget.connect_to_menu_bar(self.tab2_widgets[0], self.tab2_widgets[0])

    def closeEvent(self, *args, **kwargs):
        self.worker.stop()
        self.thread.exit()

    @staticmethod
    def connect_to_menu_bar(open_widget, save_widget):
        # Connect menu bar to widget
        all_widgets = QApplication.topLevelWidgets()
        menu_bar = next(obj for obj in all_widgets if type(obj) == MenuBar)
        menu_bar.connect_widgets(open_widget, save_widget)

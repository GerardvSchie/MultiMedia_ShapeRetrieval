import logging

from PyQt6 import QtWidgets, QtGui, QtCore
from PyQt6.QtWidgets import QTabWidget, QGridLayout, QWidget

from qt_app.util.worker import Worker
from qt_app.widget.visualization_widget import VisualizationWidget
from qt_app.gui.menu_bar import MenuBar
from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtWidgets import QMainWindow, QApplication


class TabWidget(QTabWidget):
    def __init__(self):
        super(TabWidget, self).__init__()
        self.thread = QtCore.QThread()
        self.worker = Worker()

        self.widget = QTabWidget()
        QGridLayout(self.widget)

        self.widget.addTab(self.tab_1_widget(), "Tab 1")
        # self.widget.addTab(self.tab_1_widget(), "Tab 2")
        # self.widget.addTab(self.tab_1_widget(), "Tab 3")

    def tab_1_widget(self) -> QWidget:
        # Widget 1
        scene_widget = VisualizationWidget(False)
        window = QtGui.QWindow.fromWinId(scene_widget.hwnd)
        window_container = self.createWindowContainer(window, scene_widget)

        layout = QtWidgets.QGridLayout(scene_widget)
        layout.addWidget(window_container, 0, 0)
        # self.setCentralWidget(scene_widget_1)

        # self.thread = QtCore.QThread()
        # self.worker = Worker()
        # self.thread.started.connect(lambda: self.worker.run([scene_widget]))
        # self.thread.start()

        self.active_widgets = [scene_widget]

        # Menu bar
        top_level_widgets = QApplication.topLevelWidgets()
        menu_bar = next(obj for obj in top_level_widgets if type(obj) == MenuBar)
        menu_bar.initialize(scene_widget)

        return scene_widget

    # def tab_1_widget(self) -> QWidget:
    #     # Widget 1
    #     scene_widget_1 = VisualizationWidget(False)
    #     window_1 = QtGui.QWindow.fromWinId(scene_widget_1.hwnd)
    #     window_container_1 = self.createWindowContainer(window_1, scene_widget_1)
    #
    #     # Widget 2
    #     scene_widget_2 = VisualizationWidget(True)
    #     window_2 = QtGui.QWindow.fromWinId(scene_widget_2.hwnd)
    #     window_container_2 = self.createWindowContainer(window_2, scene_widget_2)
    #
    #     btn = QtWidgets.QPushButton(text="test")
    #     btn.clicked.connect(lambda: print("Button pressed!"))
    #
    #     layout = QtWidgets.QGridLayout(scene_widget_1)
    #     layout.addWidget(window_container_1, 0, 0)
    #     layout.addWidget(window_container_2)
    #     layout.addWidget(btn)
    #     # self.setCentralWidget(scene_widget_1)
    #
    #     self.thread = QtCore.QThread()
    #     self.worker = Worker()
    #     self.thread.started.connect(lambda: self.worker.run([scene_widget_1, scene_widget_2]))
    #     self.thread.start()
    #
    #     self.active_widgets = [scene_widget_1, scene_widget_2]
    #
    #     # Menu bar
    #     top_level_widgets = QApplication.topLevelWidgets()
    #     menu_bar = next(obj for obj in top_level_widgets if type(obj) == MenuBar)
    #     menu_bar.initialize(scene_widget_1)
    #
    #     return scene_widget_1

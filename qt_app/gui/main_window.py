import logging
from PyQt6 import QtWidgets, QtGui, QtCore
from PyQt6.QtCore import QThreadPool

from qt_app.widget.tab_widget import TabWidget
from qt_app.util.worker import Worker
from qt_app.util.worker import MultiWorker
from qt_app.widget.visualization_widget import VisualizationWidget
from qt_app.gui.menu_bar import MenuBar
from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtWidgets import QMainWindow, QApplication
from PyQt6.QtGui import QIcon, QAction


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        # MenuBar()
        self.menu_bar = MenuBar(self.menuBar())

        # Tabs
        self.tab_widget = TabWidget()
        layout = QtWidgets.QGridLayout()
        self.setLayout(layout)
        layout.addWidget(self.tab_widget.widget, 0, 0)
        self.setCentralWidget(self.tab_widget.widget)

        # Body of the application
        self.active_widgets = []
        self.thread = None
        self.worker = None
        # self.mesh_visualizer_mode()

    def closeEvent(self, *args, **kwargs):
        # Close each widget
        self.worker.stop()
        self.thread.exit()

        for widget in self.active_widgets:
            widget.closeEvent(*args, **kwargs)



    # def start_vis(self):
    #     logging.info("thread start")
    #     self.scene_widget.vis.run()
    #     self.scene_widget_2.vis.run()
    #     logging.info("thread end")
    #
    # def update_vis(self):
    #     self.scene_widget.update_vis()
    #     self.scene_widget_2.update_vis()

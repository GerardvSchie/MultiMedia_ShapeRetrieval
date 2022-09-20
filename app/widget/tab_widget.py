import logging
from app.widget.settings_widget import SettingsWidget

from PyQt6 import QtWidgets, QtGui, QtCore
from PyQt6.QtWidgets import QTabWidget, QGridLayout, QWidget

from app.util.worker import Worker
from app.widget.visualization_widget import VisualizationWidget
from app.gui.menu_bar import MenuBar
from PyQt6.QtGui import QAction, QIcon, QPalette, QColor
from PyQt6.QtWidgets import QMainWindow, QApplication


class TabWidget(QTabWidget):
    def __init__(self):
        super(TabWidget, self).__init__()

        # Start thread that handles the events on o3d windows
        self.thread = QtCore.QThread()
        self.worker = Worker()
        self.thread.started.connect(lambda: self.worker.run())
        self.thread.start()

        # Tab widget
        self.widget = QTabWidget()
        QtWidgets.QHBoxLayout(self.widget)

        # Tab 1
        self.tab1_widgets = []
        self.tab1_widget = self.tab_1_widget()
        self.widget.addTab(self.tab1_widget, "Mesh inspect")

        # Tab 1
        self.tab2_widgets = []
        self.tab2_widget = self.tab_2_widget()
        self.widget.addTab(self.tab2_widget, "Mesh inspect 2")

        self.widget.currentChanged.connect(self.currentChanged)
        # Select tab 1
        self.tab_1_select()

    def currentChanged(self, index: int) -> None:
        if index == 0:
            print("Changed to tab 1")
            self.tab_1_select()
        if index == 1:
            print("Changed to tab 2")
            self.tab_2_select()

        # Try update the widget
        self.widget.update()

    def tab_1_widget(self) -> QWidget:
        settings_widget = SettingsWidget()
        settings_widget.setPalette(QPalette(QColor(100, 100, 100)))
        settings_widget.widget.setFixedWidth(150)

        scene_widget = VisualizationWidget(False)
        window = QtGui.QWindow.fromWinId(scene_widget.hwnd)
        window_container = self.createWindowContainer(window, scene_widget)

        # Assign scene widget here since that covers entire gui
        layout = QtWidgets.QHBoxLayout(scene_widget)

        layout.addWidget(settings_widget.widget)
        layout.addWidget(window_container)

        self.tab1_widgets = [scene_widget, settings_widget]
        return scene_widget

    def tab_2_widget(self) -> QWidget:
        # Widget 1
        scene_widget_1 = VisualizationWidget(False)
        window_1 = QtGui.QWindow.fromWinId(scene_widget_1.hwnd)
        window_container_1 = self.createWindowContainer(window_1, scene_widget_1)

        # Widget 2
        scene_widget_2 = VisualizationWidget(True)
        window_2 = QtGui.QWindow.fromWinId(scene_widget_2.hwnd)
        window_container_2 = self.createWindowContainer(window_2, scene_widget_2)

        btn = QtWidgets.QPushButton(text="test")
        btn.clicked.connect(lambda: print("Button pressed!"))

        layout = QtWidgets.QGridLayout(scene_widget_1)
        layout.addWidget(window_container_1, 0, 0)
        layout.addWidget(window_container_2)
        layout.addWidget(btn)

        self.tab2_widgets = [scene_widget_1, scene_widget_2]
        return scene_widget_1

    def tab_1_select(self):
        self.worker.set_scenes([self.tab1_widgets[0]])
        TabWidget.connect_to_menu_bar(self.tab2_widgets[0], self.tab2_widgets[0])

    def tab_2_select(self):
        self.worker.set_scenes(self.tab2_widgets)
        TabWidget.connect_to_menu_bar(self.tab2_widgets[0], self.tab2_widgets[0])

    def closeEvent(self, *args, **kwargs):
        self.worker.stop()
        self.thread.exit()
        #
        # for widget in self.:
        #     widget.closeEvent(*args, **kwargs)

    @staticmethod
    def connect_to_menu_bar(open_widget, save_widget):
        # Connect menu bar to widget
        top_level_widgets = QApplication.topLevelWidgets()
        menu_bar = next(obj for obj in top_level_widgets if type(obj) == MenuBar)
        menu_bar.connect_widgets(open_widget, save_widget)

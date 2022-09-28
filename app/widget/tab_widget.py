from app.widget.util import color_widget

from PyQt6 import QtCore
from PyQt6.QtWidgets import QTabWidget

from app.util.worker import Worker
from app.gui.menu_bar import MenuBar
from app.widget.tab.viewer_widget import ViewerWidget
from app.widget.tab.multi_viewer_widget import MultiViewerWidget
from app.util.os import IsMacOS

from src.object.settings import Settings
from PyQt6.QtWidgets import QApplication


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

        self.currentChanged.connect(lambda index: self.current_tab_changed(index))

        # Tab widget
        color_widget(self, [255, 0, 0])

        # Tab 1
        self.tab1_widget = ViewerWidget(self.settings)
        self.addTab(self.tab1_widget, "Mesh inspect")

        # Tab 2
        if not IsMacOS:
            self.tab2_widget = MultiViewerWidget(self.settings)
            self.addTab(self.tab2_widget, "Mesh inspect 2")

        # Select tab 1
        self.tab_1_select()

    def current_tab_changed(self, index: int):
        if index == 0:
            self.tab_1_select()
        if index == 1:
            self.tab_2_select()

        # Try update the widget
        self.update()

    def tab_1_select(self):
        self.worker.set_scenes(self.tab1_widget.scene_widgets)
        TabWidget.connect_to_menu_bar(self.tab1_widget.scene_widgets[0], self.tab1_widget.scene_widgets[0])

    def tab_2_select(self):
        self.worker.set_scenes(self.tab2_widget.scene_widgets)
        TabWidget.connect_to_menu_bar(self.tab2_widget.scene_widgets[0], self.tab2_widget.scene_widgets[0])

    def closeEvent(self, *args, **kwargs):
        self.worker.stop()
        self.thread.exit()

    @staticmethod
    def connect_to_menu_bar(open_widget, save_widget):
        # Connect menu bar to widget
        all_widgets = QApplication.topLevelWidgets()
        menu_bar = next(obj for obj in all_widgets if type(obj) == MenuBar)
        menu_bar.connect_widgets(open_widget, save_widget)

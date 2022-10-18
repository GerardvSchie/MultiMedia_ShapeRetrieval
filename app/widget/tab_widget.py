from app.widget.tab.remeshing_tab_widget import RemeshingTabWidget
from app.widget.tab.shape_features_tab_widget import ShapeFeaturesTabWidget
from app.widget.util import color_widget

from PyQt6 import QtCore
from PyQt6.QtWidgets import QTabWidget, QApplication

from app.util.worker import Worker
from app.gui.menu_bar import MenuBar
from app.widget.tab.viewer_widget import ViewerWidget
from app.widget.tab.normalization_tab_widget import NormalizationTabWidget
from app.util.os import IsMacOS
from src.database.reader import DatabaseReader
from src.object.features.shape_features import ShapeFeatures


class TabWidget(QTabWidget):
    def __init__(self):
        super(TabWidget, self).__init__()

        shape_features: dict[str, ShapeFeatures] = DatabaseReader.read_all_shape_features()

        # Connect tab to menu bar
        all_widgets = QApplication.topLevelWidgets()
        menu_bar = next(obj for obj in all_widgets if type(obj) == MenuBar)
        menu_bar.connect_tab_widget(self)

        # Start thread that handles the events on o3d windows
        self.thread = QtCore.QThread()
        self.worker = Worker()
        self.thread.started.connect(lambda: self.worker.run())
        self.thread.start()

        self.currentChanged.connect(lambda _: self.current_tab_changed())

        # Tab widget
        color_widget(self, [255, 0, 0])

        # Tab 1
        self.tab1_widget = ViewerWidget(shape_features)
        self.addTab(self.tab1_widget, "Mesh inspect")

        # Tab 2
        if not IsMacOS:
            self.tab2_widget = RemeshingTabWidget(shape_features)
            self.addTab(self.tab2_widget, "Remeshing")
            self.setCurrentWidget(self.tab2_widget)

        # Tab 3
        if not IsMacOS:
            self.tab3_widget = NormalizationTabWidget(shape_features)
            self.addTab(self.tab3_widget, "Normalize mesh")

        # Tab 4
        if not IsMacOS:
            self.tab4_widget = ShapeFeaturesTabWidget(shape_features)
            self.addTab(self.tab4_widget, "Features")

    def closeEvent(self, *args, **kwargs):
        self.worker.stop()
        self.thread.exit()

    def current_tab_changed(self):
        # Set new scenes for the worker to render
        self.worker.set_scenes(self.currentWidget().scene_widgets)
        self.update()

    def load_shape(self, file_path):
        self.currentWidget().load_shape(file_path)

    def save_shape(self, file_path):
        self.currentWidget().save_shape(file_path)

    def export_image_action(self, file_path: str):
        self.currentWidget().export_image_action(file_path)

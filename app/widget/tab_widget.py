from PyQt6 import QtCore
from PyQt6.QtWidgets import QTabWidget, QApplication

from app.util.worker import Worker
from app.gui.menu_bar import MenuBar
from app.widget.util import color_widget
from app.widget.tab.viewer_widget import ViewerWidget
from app.widget.tab.tsne_canvas_tab_widget import TsneCanvasTabWidget
from app.widget.tab.descriptors_table_tab_widget import DescriptorsTableTabWidget
from app.widget.tab.features_table_tab_widget import FeaturesTableTabWidget
from app.widget.tab.normalization_tab_widget import NormalizationTabWidget
from app.widget.tab.normalized_descriptors_table_tab_widget import NormalizedDescriptorsTableTabWidget
from app.widget.tab.query_tab_widget import QueryTabWidget
from app.widget.tab.shape_features_tab_widget import ShapeFeaturesTabWidget
from app.widget.tab.performance_tab_widget import PerformanceTabWidget


class TabWidget(QTabWidget):
    def __init__(self):
        """Create the tabs and add them to the set of tabs"""
        super(TabWidget, self).__init__()
        color_widget(self, [255, 0, 0])

        # Connect tab to menu bar
        all_widgets = QApplication.topLevelWidgets()
        menu_bar = next(obj for obj in all_widgets if type(obj) == MenuBar)
        menu_bar.connect_tab_widget(self)

        # Start thread that handles the events on o3d windows
        self.thread = QtCore.QThread()
        self.worker = Worker()
        self.thread.started.connect(lambda: self.worker.run())
        self.thread.start()

        # Connect function before tab is created
        self.currentChanged.connect(lambda _: self.current_tab_changed())

        # Tab widgets
        self.viewer_widget = ViewerWidget()
        self.normalization_widget = NormalizationTabWidget()
        self.shape_features_widget = ShapeFeaturesTabWidget()
        self.features_table_widget = FeaturesTableTabWidget()
        self.descriptors_table_widget = DescriptorsTableTabWidget()
        self.normalized_descriptors_table_widget = NormalizedDescriptorsTableTabWidget()
        self.query_widget = QueryTabWidget()
        self.tsne_widget = TsneCanvasTabWidget()
        self.performance_widget = PerformanceTabWidget()

        # Add the tabs
        self.addTab(self.viewer_widget, "Mesh inspect")
        self.addTab(self.normalization_widget, "Normalize mesh")
        self.addTab(self.shape_features_widget, "Features")
        self.addTab(self.features_table_widget, "Features table")
        self.addTab(self.descriptors_table_widget, "Descriptors table")
        self.addTab(self.normalized_descriptors_table_widget, "Normalized descriptors table")
        self.addTab(self.query_widget, "Query")
        self.addTab(self.tsne_widget, "t-SNE")
        self.addTab(self.performance_widget, "Performance")

        # Set current widget
        self.setCurrentWidget(self.tsne_widget)

    def closeEvent(self, *args, **kwargs) -> None:
        """Close the tab widget"""
        self.worker.stop()
        self.thread.exit()

    def current_tab_changed(self) -> None:
        """Set new scenes for the worker to render, empty list will block, so prevent that"""
        if self.currentWidget().scene_widgets:
            self.worker.set_scenes(self.currentWidget().scene_widgets)
            self.update()

    def load_shape_from_path(self, file_path: str) -> None:
        """When a shape gets loaded in from path, call the method of the tab to handle it

        :param file_path: Path to the shape
        """
        self.currentWidget().load_shape_from_path(file_path)

    def save_shape(self, file_path: str) -> None:
        """Save shape to the given path

        :param file_path: Path to save it to
        """
        self.currentWidget().save_shape(file_path)

    def export_image_action(self, file_path: str) -> None:
        """The current tab gets called to handle the export

        :param file_path: Path to save the image to
        """
        self.currentWidget().export_image_action(file_path)

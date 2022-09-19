import logging
import open3d as o3d
import win32gui
from PyQt6 import QtWidgets, QtGui, QtCore

from src.object.shape import Shape
from src.pipeline.feature_extractor import FeatureExtractor


class VisualizationWidget(QtWidgets.QWidget):
    def __init__(self, showWireFrame):
        super(VisualizationWidget, self).__init__()
        self.showWireFrame = showWireFrame

        self.shape = None
        self.widget = QtWidgets.QWidget()
        self.vis = o3d.visualization.VisualizerWithEditing()
        # Visible=False so it does not open separate window
        self.vis.create_window(visible=False)
        self.hwnd = win32gui.FindWindowEx(0, 0, None, "Open3D - free view")
        self.load_shape("data/example.off")

    def initialize(self):
        pass

    def closeEvent(self, *args, **kwargs):
        self.vis.close()
        # self.vis.destroy_window()

    # Part of the scene, what is in the window
    def load_shape(self, path):
        # Here the widget is initialized
        self.vis.clear_geometries()
        self.shape = Shape(path, load_shape=True)
        FeatureExtractor.extract_features(self.shape)

        if self.shape.geometry is not None:
            try:
                if self.showWireFrame:
                    render_option: o3d.visualization.RenderOption = self.vis.get_render_option()
                    render_option.mesh_show_wireframe = True

                self.vis.add_geometry(self.shape.geometry)
                # self.vis.scene.add_geometry("__model__", self.shape.geometry,
                #                                self.settings_widget.settings.material)

                # bounds = self.shape.geometry.get_axis_aligned_bounding_box()
                # self.widget.setup_camera(60, bounds, bounds.get_center())
                # self.property_widget.update_properties(self.shape.features)
            except Exception as e:
                logging.error(f"Loading of shape failed with message: {e}")

    def start_vis(self):
        self.vis.run()

    def update_vis(self):
        # self.vis.update_geometry(self.shape.geometry)
        self.vis.poll_events()
        self.vis.update_renderer()

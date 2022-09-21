import logging
import open3d as o3d
import win32gui
from PyQt6 import QtWidgets, QtGui, QtCore

from src.object.render_mode import RenderMode
from src.object.shape import Shape
from src.object.settings import Settings
from src.pipeline.feature_extractor import FeatureExtractor


class VisualizationWidget(QtWidgets.QWidget):
    def __init__(self, settings: Settings):
        super(VisualizationWidget, self).__init__()
        # self.showWireFrame = showWireFrame

        # Settings
        self.shape = None
        self.settings = settings

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
        self.vis.destroy_window()

    # Part of the scene, what is in the window
    def load_shape(self, path):
        # Here the widget is initialized
        self.vis.clear_geometries()
        self.shape = Shape(path, load_shape=True)
        FeatureExtractor.extract_features(self.shape)

        if self.shape.geometry is not None:
            try:
                self.apply_settings()
                self.vis.add_geometry(self.shape.mesh)

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

    def apply_settings(self):
        self.vis.clear_geometries()
        if self.settings.render_mode == RenderMode.POINT_CLOUD:
            self.vis.add_geometry(self.shape.point_cloud)
        else:
            render_option: o3d.visualization.RenderOption = self.vis.get_render_option()
            render_option.mesh_show_wireframe = self.settings.render_mode == RenderMode.WIREFRAME
            render_option.point_show_normal = self.settings.render_mode == RenderMode.NORMALS
            self.vis.add_geometry(self.shape.mesh)

        # if self.settings.apply_render_mode:
        #     self.vis.update_renderer()
        # self.vis.update_renderer()
        #     self.settings.apply_render_mode = False


        # view_control: o3d.visualization.ViewControl = self.vis.get_view_control()
        # view_control.
        #
        # self.vis.clear_geometries()
        # self.vis.add_geometry(self.shape.geometry)
        # renderer.
        #
        # if self.settings.apply_render_mode:
        #     self.vis.update_renderer()
        #     self.settings.apply_render_mode = False
        # else:
        #     self.vis.update_renderer()

    # def set_mouse_mode_rotate(self):
    #     view_control = self.vis.get_view_control()
    #     view_control = gui.SceneWidget.Controls.ROTATE_CAMERA
    #
    # def set_mouse_mode_fly(self):
    #     self.widget.set_view_controls(gui.SceneWidget.Controls.FLY)

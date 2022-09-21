import logging
import numpy as np
import open3d as o3d
from open3d.visualization.gui import SceneWidget
import open3d.visualization.gui as gui
import win32gui
from open3d.visualization.rendering import Open3DScene
import open3d.visualization.rendering as rendering
from open3d.visualization.gui import Application

from PyQt6 import QtWidgets

from src.object.render_mode import RenderMode
from src.object.shape import Shape
from src.object.settings import Settings
from src.pipeline.feature_extractor import FeatureExtractor


class VisualizationWidget(QtWidgets.QWidget):
    def __init__(self, settings: Settings):
        super(VisualizationWidget, self).__init__()

        # Settings
        self.shape = None
        self.settings = settings
        self.current_window_type = -1

        self.widget = QtWidgets.QWidget()
        self.vis = None
        self.vis = o3d.visualization.VisualizerWithEditing()

        # Visible=False so it does not open separate window
        self.vis.create_window(visible=False)
        self.hwnd = win32gui.FindWindowEx(0, 0, None, "Open3D - free view")
        self.load_shape("data/example.off")

    def closeEvent(self, *args, **kwargs):
        self.vis.close()
        self.vis.destroy_window()

    # Part of the scene, what is in the window
    def load_shape(self, path):
        self.shape = Shape(path, load_shape=True)
        FeatureExtractor.extract_features(self.shape)
        self.current_window_type = -1
        self.visualize_shape()
        # bounds = self.shape.geometry.get_axis_aligned_bounding_box()
        # self.widget.setup_camera(60, bounds, bounds.get_center())
        # self.property_widget.update_properties(self.shape.features)

    def start_vis(self):
        self.vis.run()

    def update_vis(self):
        # self.vis.update_geometry(self.shape.geometry)
        self.vis.poll_events()
        self.vis.update_renderer()

    def visualize_shape(self):
        # Set render options
        render_option: o3d.visualization.RenderOption = self.vis.get_render_option()
        render_option.mesh_show_wireframe = self.settings.render_mode == RenderMode.WIREFRAME
        render_option.light_on = self.settings.render_mode != RenderMode.SILHOUETTE

        # Need to reset geometry only if the window type changes
        reset_geometry = self.current_window_type != RenderMode.WINDOW_TYPE[self.settings.render_mode]
        if reset_geometry:
            self.vis.clear_geometries()

        # Handle each different type of visualization
        if self.settings.render_mode == RenderMode.POINT_CLOUD:
            if reset_geometry:
                self.vis.add_geometry(self.shape.point_cloud)
        elif self.settings.render_mode == RenderMode.SILHOUETTE:
            self.shape.mesh.paint_uniform_color([0, 0, 0])

            if reset_geometry:
                self.vis.add_geometry(self.shape.mesh)
        elif self.settings.render_mode == RenderMode.CONVEX_HULL:
            if reset_geometry:
                hull_line_set = o3d.geometry.LineSet.create_from_triangle_mesh(self.shape.convex_hull)
                hull_line_set.paint_uniform_color((1, 0, 0))
                # o3d.visualization.draw_geometries_with_editing([self.shape.point_cloud])
                # o3d.visualization.draw_geometries_with_editing([hull_line_set])
                # self.vis.add_geometry(self.shape.point_cloud)
                self.vis.add_geometry(hull_line_set)
        else:
            self.shape.mesh.paint_uniform_color([1, 1, 1])

            if reset_geometry:
                self.vis.add_geometry(self.shape.mesh)

        # Update the window type to the latest
        self.current_window_type = RenderMode.WINDOW_TYPE[self.settings.render_mode]
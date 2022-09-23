import logging
import open3d as o3d
import open3d.visualization.gui as gui
import win32gui

from PyQt6.QtWidgets import QWidget

from src.object.shape import Shape
from src.object.settings import Settings
from src.pipeline.feature_extractor import FeatureExtractor
from app.widget.features_widget import FeaturesWidget


class VisualizationWidget(QWidget):
    def __init__(self, settings: Settings):
        super(VisualizationWidget, self).__init__()
        self.shape = None
        self.features_widget = None
        self.hull_line_set = None

        # Settings and state
        self.settings = settings
        self._background_color = gui.Color(1, 1, 1)
        self._mesh_color = gui.Color(1, 1, 1)
        self._convex_hull_color = gui.Color(1, 0, 0)
        self._light_on = True
        self._show_mesh = False
        self._show_wireframe = False
        self._show_point_cloud = False
        self._show_convex_hull = False
        self._show_axes = False

        self.vis = o3d.visualization.Visualizer()

        # Visible=False so it does not open separate window for a moment
        self.vis.create_window(visible=False)
        self.hwnd = win32gui.FindWindowEx(0, 0, None, "Open3D")
        self.load_shape("data/example.off")

    def connect_features(self, features_widget: FeaturesWidget):
        self.features_widget = features_widget

    def closeEvent(self, *args, **kwargs):
        self.vis.close()
        self.vis.destroy_window()

    # Part of the scene, what is in the window
    def load_shape(self, path):
        # Clear geometries and update state
        self.vis.clear_geometries()
        self.clear_geometries_state()

        # Load shape
        self.shape = Shape(path, load_geometries=True)
        FeatureExtractor.extract_features(self.shape)
        self.visualize_shape()

        # Only update features if there is one connected
        if self.features_widget:
            self.features_widget.update_values(self.shape.features)

        # bounds = self.shape.geometry.get_axis_aligned_bounding_box()
        # self.widget.setup_camera(60, bounds, bounds.get_center())
        # self.property_widget.update_properties(self.shape.features)

    def start_vis(self):
        self.vis.run()

    def update_vis(self):
        self.vis.poll_events()
        self.vis.update_renderer()

    def clear_geometries_state(self):
        self._show_mesh = False
        self._show_wireframe = False
        self._show_point_cloud = False
        self._show_convex_hull = False
        self._show_axes = False

    def update_state(self):
        self._background_color = self.settings.background_color
        self._mesh_color = self.settings.mesh_color
        self._convex_hull_color = self.settings.convex_hull_color

        # Render settings
        self._light_on = self.settings.light_on
        self._show_mesh = self.settings.show_mesh
        self._show_wireframe = self.settings.show_wireframe
        self._show_point_cloud = self.settings.show_point_cloud
        self._show_convex_hull = self.settings.show_convex_hull
        self._show_axes = self.settings.show_axes

    def visualize_shape(self):
        # Set render options
        render_option: o3d.visualization.RenderOption = self.vis.get_render_option()
        render_option.mesh_show_wireframe = self.settings.show_wireframe
        render_option.light_on = self.settings.light_on

        # Handle each different type of visualization
        self._resolve_geometry_state_difference(self._show_mesh, self.settings.show_mesh, self.shape.geometries.mesh)
        self._resolve_geometry_state_difference(self._show_point_cloud, self.settings.show_point_cloud, self.shape.geometries.point_cloud)
        self._resolve_geometry_state_difference(self._show_convex_hull, self.settings.show_convex_hull, self.shape.geometries.convex_hull_line_set)
        self._resolve_geometry_state_difference(self._show_axes, self.settings.show_axes, self.shape.geometries.axes)
        # TODO: self.shape.mesh.paint_uniform_color([1, 1, 1])

        # Update the state of the widget to the current state
        self.update_state()
        self.vis.update_renderer()

    def _resolve_geometry_state_difference(self, old_state, new_state, geometry):
        if not geometry:
            logging.warning("Trying to update a geometry that is not present")
            return

        # No difference of state to resolve
        if old_state == new_state:
            return

        # New state adds geometry
        if not old_state and new_state:
            self.vis.add_geometry(geometry)
        # Geometry was present, remove it
        else:
            self.vis.remove_geometry(geometry)

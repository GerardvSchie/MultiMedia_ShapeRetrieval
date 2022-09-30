import logging
import open3d as o3d
import open3d.visualization
import win32gui

from PyQt6.QtWidgets import QWidget

from src.controller.geometries_controller import GeometriesController
from src.object.shape import Shape
from src.object.settings import Settings
from app.util.os import IsMacOS


class VisualizationWidget(QWidget):
    def __init__(self, settings: Settings):
        super(VisualizationWidget, self).__init__()
        # Trying to set aspect ratio
        self.setMinimumSize(400, 400)

        # Trying to set aspect ratio through size policy
        # size_policy = QSizePolicy()
        # size_policy.setWidthForHeight(True)
        # self.setSizePolicy(size_policy)

        self.shape: Shape = None

        # Settings and state
        self.settings: Settings = settings
        self._background_color: [float] = (1, 1, 1)
        self._mesh_color: [float] = (1, 1, 1)

        self._show_mesh: bool = False
        self._show_point_cloud: bool = False
        self._show_convex_hull: bool = False
        self._show_axis_aligned_bounding_box: bool = False
        self._show_center_mesh: bool = False

        self._show_silhouette: bool = False
        self._show_axes: bool = False
        self._axes = GeometriesController.get_coordinate_axes()

        self.vis: open3d.visualization.Visualizer = o3d.visualization.Visualizer()

        # Visible=False so it does not open separate window for a moment
        self.vis.create_window(visible=IsMacOS)

        if not IsMacOS:
            self.hwnd = win32gui.FindWindowEx(0, 0, None, "Open3D")

        self.load_shape("data/example.off")

    def closeEvent(self, *args, **kwargs):
        self.vis.close()
        self.vis.destroy_window()

    # Part of the scene, what is in the window
    def load_shape(self, path):
        # Clear geometries and update state
        self.clear()

        # Load shape
        self.shape = Shape(path, load_geometries=True)
        GeometriesController.calculate_mesh_normals(self.shape.geometries, True)
        GeometriesController.calculate_point_cloud_normals(self.shape.geometries, True)

        if self.settings.show_silhouette:
            self.shape.geometries.mesh.paint_uniform_color((0, 0, 0))
        else:
            self.shape.geometries.mesh.paint_uniform_color(self.settings.mesh_color)
        self.update_widget()

        # bounds = self.shape.geometry.get_axis_aligned_bounding_box()
        # self.widget.setup_camera(60, bounds, bounds.get_center())
        # self.property_widget.update_properties(self.shape.features)

    def clear(self):
        self.vis.clear_geometries()
        # Update state
        self._show_mesh = False
        self._show_point_cloud = False
        self._show_convex_hull = False
        self._show_axis_aligned_bounding_box = False
        self._show_axes = False
        self._show_center_mesh = False

    def start_vis(self):
        self.vis.run()

    def update_vis(self):
        self.vis.poll_events()
        self.vis.update_renderer()

    def update_state(self):
        # Colors
        self._background_color = self.settings.background_color
        self._mesh_color = self.settings.mesh_color

        # Render settings
        self._show_mesh = self.settings.show_mesh
        self._show_point_cloud = self.settings.show_point_cloud
        self._show_convex_hull = self.settings.show_convex_hull
        self._show_axis_aligned_bounding_box = self.settings.show_axis_aligned_bounding_box
        self._show_center_mesh = self.settings.show_center_mesh

        # Additional options
        self._show_silhouette = self.settings.show_silhouette
        self._show_axes = self.settings.show_axes

    def update_widget(self):
        # Set render options
        render_option: o3d.visualization.RenderOption = self.vis.get_render_option()
        render_option.mesh_show_wireframe = self.settings.show_wireframe and not self.settings.show_silhouette
        render_option.point_show_normal = self.settings.show_normals
        render_option.light_on = not self.settings.show_silhouette
        if self.settings.show_silhouette:
            render_option.background_color = [255] * 3
        else:
            render_option.background_color = self.settings.background_color

        self._resolve_mesh_color_difference(self._mesh_color, self.settings.mesh_color)

        # Handle each different type of visualization
        self._resolve_geometry_state_difference(self._show_mesh, self.settings.show_mesh, self.shape.geometries.mesh)
        self._resolve_geometry_state_difference(self._show_point_cloud, self.settings.show_point_cloud, self.shape.geometries.point_cloud)
        self._resolve_geometry_state_difference(self._show_convex_hull, self.settings.show_convex_hull, self.shape.geometries.convex_hull_line_set)
        self._resolve_geometry_state_difference(self._show_axis_aligned_bounding_box, self.settings.show_axis_aligned_bounding_box, self.shape.geometries.axis_aligned_bounding_box_line_set)
        self._resolve_geometry_state_difference(self._show_axes, self.settings.show_axes, self._axes)
        self._resolve_geometry_state_difference(self._show_center_mesh, self.settings.show_center_mesh, self.shape.geometries.center_mesh)

        # Silhouette mode
        self._resolve_silhouette_state_difference(self._show_silhouette, self.settings.show_silhouette)

        # Update the state of the widget to the current state
        self.update_state()
        self.vis.update_renderer()

    def _resolve_mesh_color_difference(self, old_color, new_color):
        if old_color == new_color:
            return

        if self._show_silhouette:
            return

        self.shape.geometries.mesh.paint_uniform_color(self.settings.mesh_color)
        self.vis.update_geometry(self.shape.geometries.mesh)

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

    def _resolve_silhouette_state_difference(self, old_state, new_state):
        # No difference of state to resolve
        if old_state == new_state:
            return

        # Switch to silhouette mode
        if not old_state and new_state:
            self.shape.geometries.mesh.paint_uniform_color((0, 0, 0))
            self.vis.update_geometry(self.shape.geometries.mesh)
        # Back to normal visualization mode
        else:
            self.shape.geometries.mesh.paint_uniform_color(self.settings.mesh_color)
            self.vis.update_geometry(self.shape.geometries.mesh)

import logging
import open3d as o3d
import open3d.visualization
import win32gui

from PyQt6.QtWidgets import QWidget

from src.controller.geometries_controller import GeometriesController
from src.object.shape import Shape
from src.object.settings import Settings


class VisualizationWidget(QWidget):
    """
    Visualization widget work with states, a current state and a desired state
    If the two states do not match the actions are taken to resolve the difference

    Example: If the desired state shows a convex hull and the current state does not
    It resolves it by adding the convex hull mesh object to the scene
    """
    def __init__(self, settings: Settings, mesh_mode=False, convex_hull_mode=False, silhouette_mode=False):
        """Create the visualization widget and the handler.
        Contains current settings and desired settings

        :param settings: Current settings the widget should have
        :param mesh_mode: Whether it must keep showing the mesh
        :param convex_hull_mode: Whether it must keep showing a convex hull
        :param silhouette_mode: Whether it remains showing a silhouette
        """
        super(VisualizationWidget, self).__init__()
        self.setMinimumSize(400, 400)

        # Trying to set aspect ratio through size policy
        # size_policy = QSizePolicy()
        # size_policy.setWidthForHeight(True)
        # self.setSizePolicy(size_policy)

        self.shape: Shape = None

        # Current and desired state
        self.desired_settings: Settings = settings
        self.current_settings: Settings = Settings()

        # Modes will ensure the mesh, hull or silhouette mode is always shown
        self.mesh_mode = mesh_mode
        self.convex_hull_mode = convex_hull_mode
        self.silhouette_mode = silhouette_mode

        # Create relevant handlers and objects and update the scene
        self._axes = GeometriesController.get_coordinate_axes()
        self.vis: open3d.visualization.Visualizer = o3d.visualization.Visualizer()

        # Visible=False so it does not open separate window for a moment
        self.vis.create_window(visible=False)
        self.hwnd = win32gui.FindWindowEx(0, 0, None, "Open3D")
        self.focusWidget()
        self.update_widget()

    def closeEvent(self, *args, **kwargs) -> None:
        """Close the widget"""
        self.vis.close()
        self.vis.destroy_window()

    def load_shape_from_path(self, path) -> None:
        """Create shape object from path and show it in the scene

        :param path: Path of the shape to load
        """
        self.load_shape(Shape(path, load_geometries=True))

    def load_shape(self, shape) -> None:
        """Load shape object into

        :param shape: Shape to load into the scene
        """
        # Clear geometries and update state
        self.clear()

        # Load shape + the geometries needed for GUI drawing
        self.shape = shape
        GeometriesController.calculate_gui_geometries(self.shape.geometries)

        # Compute normals of point cloud and mesh
        GeometriesController.calculate_mesh_normals(self.shape.geometries, True)
        GeometriesController.calculate_point_cloud_normals(self.shape.geometries, True)

        # Paint mesh based on whether the silhouette needs to be shown
        if self.desired_settings.show_silhouette:
            self.shape.geometries.mesh.paint_uniform_color((0, 0, 0))
        else:
            self.shape.geometries.mesh.paint_uniform_color(self.desired_settings.mesh_color)
            self.current_settings.mesh_color = self.desired_settings.mesh_color

        # Update scene
        self.update_widget()

    def clear(self) -> None:
        """Clear the shapes from the scene and update the settings"""
        self.vis.clear_geometries()
        self.current_settings.clear_meshes()

    def start_vis(self) -> None:
        """Run the visualization window"""
        self.vis.run()

    def update_vis(self) -> None:
        """Updates the scene"""
        self.vis.poll_events()
        self.vis.update_renderer()

    def update_view(self) -> None:
        """Update view point of the camera in the scene"""
        view_control: o3d.visualization.ViewControl = self.vis.get_view_control()
        ref_view = view_control.convert_to_pinhole_camera_parameters()
        print('-----')
        print('extrinsic', ref_view.extrinsic)
        print('intrinsic', ref_view.intrinsic)

    def update_widget(self) -> None:
        """Update the widget and all the state differences whether to show mesh, point cloud etc.

        Works with state difference, if currently the mesh is not in the scene
        And scene settings indicate the mesh is in the scene then the state difference resolver will add the mesh
        """
        # Cannot update widget if there is no shape
        if not self.shape:
            return

        # Update render options and set the color
        self.update_render_options()
        self._resolve_mesh_color_difference(self.current_settings.mesh_color, self.desired_settings.mesh_color)

        # Handle each different type of visualization
        self._resolve_geometry_state_difference(self.current_settings.show_mesh, (self.desired_settings.show_mesh or self.mesh_mode or self.silhouette_mode) and not self.convex_hull_mode, self.shape.geometries.mesh)
        self._resolve_geometry_state_difference(self.current_settings.show_point_cloud, self.desired_settings.show_point_cloud, self.shape.geometries.point_cloud)
        self._resolve_geometry_state_difference(self.current_settings.show_convex_hull, self.desired_settings.show_convex_hull or self.convex_hull_mode, self.shape.geometries.convex_hull_line_set)
        self._resolve_geometry_state_difference(self.current_settings.show_axis_aligned_bounding_box, self.desired_settings.show_axis_aligned_bounding_box, self.shape.geometries.axis_aligned_bounding_box_line_set)
        self._resolve_geometry_state_difference(self.current_settings.show_axes, self.desired_settings.show_axes, self._axes)
        self._resolve_geometry_state_difference(self.current_settings.show_center_mesh, self.desired_settings.show_center_mesh, self.shape.geometries.center_mesh)

        # Silhouette mode
        self._resolve_silhouette_state_difference(self.current_settings.show_silhouette, self.desired_settings.show_silhouette or self.silhouette_mode)

        # Update the state of the widget to the current state
        self.current_settings.update(self.desired_settings)
        self.vis.update_renderer()

    def update_render_options(self) -> None:
        """Sets the render options"""
        render_option: o3d.visualization.RenderOption = self.vis.get_render_option()

        # Wireframe settings
        render_option.mesh_show_wireframe = self.desired_settings.show_wireframe and not self.desired_settings.show_silhouette and not self.silhouette_mode

        # Point cloud
        render_option.point_show_normal = self.desired_settings.show_normals
        render_option.point_size = self.desired_settings.point_size

        # Silhouette
        render_option.light_on = not self.desired_settings.show_silhouette and not self.silhouette_mode
        if self.desired_settings.show_silhouette or self.silhouette_mode:
            render_option.background_color = [255] * 3
        else:
            render_option.background_color = self.desired_settings.background_color

    def _resolve_mesh_color_difference(self, old_color: [float], new_color: [float]) -> None:
        """Resolves a mesh color difference

        :param old_color: Current color of the mesh
        :param new_color: Color to change to
        :return:
        """
        # The current color is already correct
        if old_color == new_color:
            return

        # Silhouette does not change the mesh color
        if self.current_settings.show_silhouette or self.silhouette_mode:
            return

        self.shape.geometries.mesh.paint_uniform_color(self.desired_settings.mesh_color)
        self.vis.update_geometry(self.shape.geometries.mesh)

    def _resolve_geometry_state_difference(self, old_state: bool, new_state: bool, geometry: o3d.geometry) -> None:
        """Resolves state difference in geometry, whether the geometry needs to be shown or hidden

        :param old_state: Whether the mesh is shown currently
        :param new_state: Whether the desired state is to show the mesh
        :param geometry: Geometry to add or remove from the scene
        """
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

    def _resolve_silhouette_state_difference(self, old_state: bool, new_state: bool) -> None:
        """When the desired state is different from the current state
        Paints shape uniform black color when the silhouette mode is on

        :param old_state: Whether current state of the visualization widget is on silhouette mode
        :param new_state: Whether to enable silhouette mode
        """
        # No difference of state to resolve
        if old_state == new_state:
            return

        # Switch to silhouette mode
        if not old_state and new_state:
            self.shape.geometries.mesh.paint_uniform_color((0, 0, 0))
            self.vis.update_geometry(self.shape.geometries.mesh)
        # Back to normal visualization mode
        else:
            self.shape.geometries.mesh.paint_uniform_color(self.desired_settings.mesh_color)
            self.vis.update_geometry(self.shape.geometries.mesh)

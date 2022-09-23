import open3d as o3d
import win32gui

from PyQt6.QtWidgets import QWidget

from src.object.render_mode import RenderMode
from src.object.shape import Shape
from src.object.settings import Settings
from src.pipeline.feature_extractor import FeatureExtractor
from app.widget.features_widget import FeaturesWidget


class VisualizationWidget(QWidget):
    def __init__(self, settings: Settings):
        super(VisualizationWidget, self).__init__()

        # Settings
        self.shape = None
        self.features_widget = None
        self.settings = settings
        self.current_window_type = -1

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
        self.shape = Shape(path, load_shape=True)
        FeatureExtractor.extract_features(self.shape)
        self.current_window_type = -1
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
        # self.vis.update_geometry(self.shape.geometry)
        self.vis.poll_events()
        self.vis.update_renderer()

    def visualize_shape(self):
        # Set render options
        render_option: o3d.visualization.RenderOption = self.vis.get_render_option()
        render_option.mesh_show_wireframe = self.settings.render_mode == RenderMode.WIREFRAME
        render_option.light_on = self.settings.render_mode != RenderMode.SILHOUETTE
        render_option.show_coordinate_frame = self.settings.show_axes
        print(f"TODO: show coordinate frame: " + str(render_option.show_coordinate_frame))

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
                self.vis.add_geometry(self.shape.mesh.create_coordinate_frame(0.1))
                self.vis.add_geometry(self.shape.point_cloud)
                self.vis.add_geometry(hull_line_set)
        else:
            self.shape.mesh.paint_uniform_color([1, 1, 1])

            if reset_geometry:
                # self.vis.add_geometry(self.shape.mesh.create_coordinate_frame())
                self.vis.add_geometry(self.shape.mesh)

        # Update the window type to the latest
        self.current_window_type = RenderMode.WINDOW_TYPE[self.settings.render_mode]
        self.vis.update_renderer()

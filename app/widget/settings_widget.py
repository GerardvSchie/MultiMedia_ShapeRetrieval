from PyQt6.QtWidgets import QWidget, QCheckBox

from src.object.settings import Settings
from app.widget.util import color_widget
from app.layout.grid_layout import GridLayout
from app.other.color_button import ColorButton


class SettingsWidget(QWidget):
    def __init__(self, settings: Settings):
        super(SettingsWidget, self).__init__()
        color_widget(self, [0, 255, 255])

        # Widget state of main app window and the scene that is controlled by the settings
        self.settings = settings
        self.visualizer_widget = None

        # Geometries checkboxes
        show_mesh_checkbox = QCheckBox(self)
        show_mesh_checkbox.setChecked(True)
        show_mesh_checkbox.stateChanged.connect(lambda state: self._on_show_mesh(state))
        show_point_cloud_checkbox = QCheckBox(self)
        show_point_cloud_checkbox.stateChanged.connect(lambda state: self._on_show_point_cloud(state))
        show_convex_hull_checkbox = QCheckBox(self)
        show_convex_hull_checkbox.stateChanged.connect(lambda state: self._on_show_convex_hull(state))
        show_axis_aligned_bounding_box_checkbox = QCheckBox(self)
        show_axis_aligned_bounding_box_checkbox.stateChanged.connect(lambda state: self._on_show_axis_aligned_bounding_box(state))

        # Additional options
        silhouette_checkbox = QCheckBox(self)
        silhouette_checkbox.stateChanged.connect(lambda state: self._on_show_silhouette(state))
        show_wireframe_checkbox = QCheckBox(self)
        show_wireframe_checkbox.stateChanged.connect(lambda state: self._on_show_wireframe(state))
        show_axes_checkbox = QCheckBox(self)
        show_axes_checkbox.stateChanged.connect(lambda state: self._on_show_axes(state))

        color_button = ColorButton()
        color_button.connect_settings(self)

        # Create layout
        layout: GridLayout = GridLayout()
        layout.add_header("Settings")
        layout.add_row("Mesh:", show_mesh_checkbox)
        layout.add_row("Point cloud:", show_point_cloud_checkbox)
        layout.add_row("Convex hull:", show_convex_hull_checkbox)
        layout.add_row("Box:", show_axis_aligned_bounding_box_checkbox)
        layout.add_section("Additional")
        layout.add_row("Silhouette:", silhouette_checkbox)
        layout.add_row("Wireframe:", show_wireframe_checkbox)
        layout.add_row("Axes:", show_axes_checkbox)
        layout.addWidget(color_button, 1, 3)
        self.setLayout(layout)

    def connect_visualizer(self, visualizer_widget):
        self.visualizer_widget = visualizer_widget

    def apply_settings(self):
        self.visualizer_widget.visualize_shape()

    def _on_background_color(self, new_color):
        self.settings.background_color = new_color
        self.apply_settings()

    def _on_mesh_color(self, new_color):
        self.settings.mesh_color = new_color
        self.apply_settings()

    # All of these are checkboxes
    # 2 == checked and 0 == unchecked
    def _on_show_silhouette(self, state):
        self.settings.show_silhouette = state == 2
        self.apply_settings()

    def _on_show_wireframe(self, state):
        self.settings.show_wireframe = state == 2
        self.apply_settings()

    def _on_show_mesh(self, state):
        self.settings.show_mesh = state == 2
        self.apply_settings()

    def _on_show_point_cloud(self, state):
        self.settings.show_point_cloud = state == 2
        self.apply_settings()

    def _on_show_convex_hull(self, state):
        self.settings.show_convex_hull = state == 2
        self.apply_settings()

    def _on_show_axis_aligned_bounding_box(self, state):
        self.settings.show_axis_aligned_bounding_box = state == 2
        self.apply_settings()

    def _on_show_axes(self, state):
        self.settings.show_axes = state == 2
        self.apply_settings()

    # def _on_material_color(self, color):
    #     self.settings.base_color = [
    #         color.red, color.green, color.blue, color.alpha
    #     ]
    #     self.settings.apply_material = True
    #     self._apply()
    #
    # def _on_point_size(self, size):
    #     self.settings.render_mode.point_size = int(size)
    #     self.settings.apply_material = True
    #     self._apply()

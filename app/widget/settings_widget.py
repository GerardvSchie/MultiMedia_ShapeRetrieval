import logging

from PyQt6.QtWidgets import QWidget, QCheckBox

from src.object.settings import Settings
from app.widget.util import color_widget
from app.layout.grid_layout import GridLayout
from app.other.color_button import ColorButton
from app.other.toggle_button import ToggleButton
from app.other.spin_box import SpinBox


class SettingsWidget(QWidget):
    def __init__(self, settings: Settings):
        super(SettingsWidget, self).__init__()
        color_widget(self, [0, 255, 255])
        self.setFixedWidth(190)

        # Widget state of main app window and the scene that is controlled by the settings
        self.settings = settings
        self.visualizer_widgets = []

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
        show_axes_checkbox = QCheckBox(self)
        show_axes_checkbox.stateChanged.connect(lambda state: self._on_show_axes(state))

        # Color buttons
        mesh_color_button = ColorButton(True)
        mesh_color_button.connect_settings(self)
        background_color_button = ColorButton(False)
        background_color_button.connect_settings(self)

        # Toggle buttons
        wireframe_button = ToggleButton("app/icon/triangle.png")
        wireframe_button.clicked.connect(lambda state: self._on_show_wireframe(state))
        normals_button = ToggleButton("app/icon/arrow.png")
        normals_button.clicked.connect(lambda state: self._on_show_normals(state))
        center_button = ToggleButton("app/icon/center.png")
        center_button.clicked.connect(lambda state: self._on_show_center_mesh(state))

        # Point cloud size
        point_size_spin_box = SpinBox()
        point_size_spin_box.valueChanged.connect(lambda state: self._on_point_size(state))

        # Create layout
        layout: GridLayout = GridLayout()
        layout.add_header("Settings")
        layout.add_row("Mesh:", [show_mesh_checkbox, center_button, wireframe_button, mesh_color_button])
        layout.add_row("Point cloud:", [show_point_cloud_checkbox, normals_button, point_size_spin_box])
        layout.add_row("Convex hull:", [show_convex_hull_checkbox])
        layout.add_row("Box:", [show_axis_aligned_bounding_box_checkbox])
        layout.add_section("Additional")
        layout.add_row("Silhouette:", [silhouette_checkbox])
        layout.add_row("Axes:", [show_axes_checkbox])
        layout.add_row("Background:", [background_color_button])
        self.setLayout(layout)

    def connect_visualizers(self, visualizer_widgets):
        self.visualizer_widgets = visualizer_widgets
        if len(self.visualizer_widgets) < 1:
            logging.warning("List of visualizers attached to the settings is empty")

    def apply_settings(self):
        for visualizer_widget in self.visualizer_widgets:
            visualizer_widget.update_widget()

    # Method called by color button
    def _on_background_color(self, new_color):
        self.settings.background_color = new_color
        self.apply_settings()

    def _on_mesh_color(self, new_color):
        self.settings.mesh_color = new_color
        self.apply_settings()

    # Push buttons
    # True == checked and False == unchecked
    def _on_show_wireframe(self, state: bool):
        self.settings.show_wireframe = state
        self.apply_settings()

    def _on_show_normals(self, state: bool):
        self.settings.show_normals = state
        self.apply_settings()

    def _on_show_center_mesh(self, state: bool):
        self.settings.show_center_mesh = state
        self.apply_settings()

    # Spin box
    def _on_point_size(self, state: int):
        self.settings.point_size = state
        self.apply_settings()

    # All of these are checkboxes
    # 2 == checked and 0 == unchecked
    def _on_show_silhouette(self, state):
        self.settings.show_silhouette = state == 2
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

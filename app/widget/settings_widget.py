from src.object.settings import Settings
from app.widget.util import color_widget

from PyQt6.QtWidgets import QWidget, QLabel, QCheckBox, QGridLayout
from PyQt6.QtCore import Qt
from app.util.font import BOLD_FONT


class SettingsWidget(QWidget):
    def __init__(self, settings: Settings):
        super(SettingsWidget, self).__init__()
        color_widget(self, [0, 255, 255])

        # Widget state of main app window and the scene that is controlled by the settings
        self.settings = settings
        self.visualizer_widget = None

        # Header
        header_label = QLabel("Settings")
        header_label.setFont(BOLD_FONT)
        header_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Show mesh
        show_mesh_label = QLabel("Mesh:")
        show_mesh_checkbox = QCheckBox(self)
        show_mesh_checkbox.setChecked(True)
        show_mesh_checkbox.stateChanged.connect(lambda state: self._on_show_mesh(state))

        # Show point cloud
        show_point_cloud_label = QLabel("Point cloud:")
        show_point_cloud_checkbox = QCheckBox(self)
        show_point_cloud_checkbox.stateChanged.connect(lambda state: self._on_show_point_cloud(state))

        # Show convex hull
        show_convex_hull_label = QLabel("Convex hull:")
        show_convex_hull_checkbox = QCheckBox(self)
        show_convex_hull_checkbox.stateChanged.connect(lambda state: self._on_show_convex_hull(state))

        # Show axes
        show_axes_label = QLabel("Axes:")
        show_axes_checkbox = QCheckBox(self)
        show_axes_checkbox.stateChanged.connect(lambda state: self._on_show_axes(state))

        # Create layout
        layout: QGridLayout = QGridLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout.addWidget(header_label, 0, 0, 1, -1)
        layout.addWidget(show_mesh_label, 1, 0)
        layout.addWidget(show_mesh_checkbox, 1, 1)
        layout.addWidget(show_point_cloud_label, 2, 0)
        layout.addWidget(show_point_cloud_checkbox, 2, 1)
        layout.addWidget(show_convex_hull_label, 3, 0)
        layout.addWidget(show_convex_hull_checkbox, 3, 1)
        layout.addWidget(show_axes_label, 4, 0)
        layout.addWidget(show_axes_checkbox, 4, 1)

        self.setLayout(layout)

    def connect_visualizer(self, visualizer_widget):
        self.visualizer_widget = visualizer_widget

    def _apply(self):
        self.visualizer_widget.visualize_shape()

    def _on_background_color(self, new_color):
        self.settings.background_color = new_color
        self._apply()

    def _on_mesh_color(self, new_color):
        self.settings.mesh_color = new_color
        self._apply()

    def _on_convex_hull_color(self, new_color):
        self.settings.convex_hull_color = new_color
        self._apply()

    # All of these are checkboxes
    # 2 == checked and 0 == unchecked
    def _on_light(self, state):
        self.settings.light_on = state == 2
        self._apply()

    def _on_show_mesh(self, state):
        self.settings.show_mesh = state == 2
        self._apply()

    def _on_show_wireframe(self, state):
        self.settings.show_wireframe = state == 2
        self._apply()

    def _on_show_point_cloud(self, state):
        self.settings.show_point_cloud = state == 2
        self._apply()

    def _on_show_convex_hull(self, state):
        self.settings.show_convex_hull = state == 2
        self._apply()

    def _on_show_axes(self, state):
        self.settings.show_axes = state == 2
        self._apply()

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

import logging

from PyQt6.QtGui import QFont

from src.object.settings import Settings
from src.object.render_mode import RenderMode

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QComboBox, QLabel, QCheckBox
from PyQt6.QtCore import Qt
from app.util.general import BOLD_FONT


class SettingsWidget(QWidget):
    def __init__(self, settings: Settings):
        super(SettingsWidget, self).__init__()
        # Widget state of main app window and the scene that is controlled by the settings
        self.settings = settings
        self.visualizer_widget = None

        # Header
        header_label = QLabel("Settings")
        header_label.setFont(BOLD_FONT)
        header_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Render mode combobox
        render_mode_label = QLabel("Render type:")
        render_mode_combobox = QComboBox(self)
        render_mode_combobox.addItems(RenderMode.ALL)
        render_mode_combobox.currentIndexChanged.connect(lambda index: self._on_shader_change(index))

        # Show axes control
        # show_axes_label = QLabel("Show axes:")
        # show_axes_checkbox = QCheckBox(self)
        # show_axes_checkbox.stateChanged.connect(lambda state: self._on_show_axes(state))

        # Create layout
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout.addWidget(header_label)
        layout.addWidget(render_mode_label)
        layout.addWidget(render_mode_combobox)
        # layout.addWidget(show_axes_label)
        # layout.addWidget(show_axes_checkbox)

        self.setLayout(layout)

    def connect_visualizer(self, visualizer_widget):
        self.visualizer_widget = visualizer_widget

    def _apply_and_save(self):
        self.visualizer_widget.visualize_shape()

    def _on_shader_change(self, index):
        self.settings.set_render_mode(RenderMode.ALL[index])
        self.visualizer_widget.visualize_shape()

    def _on_bg_color(self, new_color):
        self.settings.bg_color = new_color
        self._apply_and_save()

    def _on_show_axes(self, state):
        # 2 == checked and 0 == unchecked
        self.settings.show_axes = state == 2
        self._apply_and_save()

    def _on_material_color(self, color):
        self.settings.render_mode.base_color = [
            color.red, color.green, color.blue, color.alpha
        ]
        self.settings.apply_material = True
        self._apply_and_save()

    def _on_point_size(self, size):
        self.settings.render_mode.point_size = int(size)
        self.settings.apply_material = True
        self._apply_and_save()

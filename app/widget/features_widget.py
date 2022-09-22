import logging
from src.object.features import Features

from PyQt6 import QtWidgets, QtGui, QtCore
from PyQt6.QtWidgets import QTabWidget, QGridLayout, QWidget, QVBoxLayout, QComboBox, QLabel
from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtWidgets import QMainWindow, QApplication


class FeaturesWidget(QWidget):
    def __init__(self):
        super(FeaturesWidget, self).__init__()
        # Widget state of main app window and the scene that is controlled by the settings
        self.features: Features = None

        # Widget
        self.widget = QWidget()
        # Render mode combobox
        render_mode_combobox = QLabel("Class")

        # Create layout
        layout = QGridLayout()
        layout.addWidget(render_mode_combobox)
        self.widget.setLayout(layout)

    def connect_features(self, features):
        self.features = features
        # Button events
        # self._arcball_button.set_on_clicked(self.scene_widget.set_mouse_mode_rotate)
        # self._fly_button.set_on_clicked(self.scene_widget.set_mouse_mode_fly)
        # self._model_button.set_on_clicked(self.scene_widget.set_mouse_mode_model)
        # self._sun_button.set_on_clicked(self.scene_widget.set_mouse_mode_sun)
        # self._ibl_button.set_on_clicked(self.scene_widget.set_mouse_mode_ibl)

    def _save_state(self):
        pass
        # self._bg_color.color_value = self.settings.bg_color
        # self._show_axes.checked = self.settings.show_axes
        # self._material_prefab.enabled = (
        #     self.settings.render_mode.shader == Settings.LIT)
        # c = gui.Color(self.settings.render_mode.base_color[0],
        #               self.settings.render_mode.base_color[1],
        #               self.settings.render_mode.base_color[2],
        #               self.settings.render_mode.base_color[3])
        # self._material_color.color_value = c
        # self._point_size.double_value = self.settings.material.point_size

    def _apply_and_save(self):
        self.visualizer_widget.visualize_shape()
        # self._save_state()

    def _on_shader_change(self, index):
        self.settings.set_render_mode(RenderMode.ALL[index])
        self.visualizer_widget.visualize_shape()

    def _on_bg_color(self, new_color):
        self.settings.bg_color = new_color
        self._apply_and_save()

    def _on_show_skybox(self, show):
        self.settings.show_skybox = show
        self._apply_and_save()

    def _on_show_axes(self, show):
        self.settings.show_axes = show
        self._apply_and_save()

    def _on_sun_color(self, color):
        self.settings.sun_color = color
        self._apply_and_save()

    def _on_material_prefab(self, name, _):
        self.settings.apply_material_prefab(name)
        self.settings.apply_material = True
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

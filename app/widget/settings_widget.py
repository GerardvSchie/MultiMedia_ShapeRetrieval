import glob
import os
import open3d.visualization.gui as gui

from src.object.settings import Settings
import logging

from PyQt6 import QtWidgets, QtGui, QtCore
from PyQt6.QtWidgets import QTabWidget, QGridLayout, QWidget, QVBoxLayout, QComboBox
from PyQt6.QtCore import QThreadPool

from app.util.worker import Worker
from app.util.worker import MultiWorker
from app.widget.visualization_widget import VisualizationWidget
from app.gui.menu_bar import MenuBar
from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtWidgets import QMainWindow, QApplication


class SettingsWidget(QWidget):
    MATERIAL_NAMES = ["Lit", "Unlit", "Normals", "Depth", "Silhouette"]
    MATERIAL_SHADERS = [
        Settings.LIT, Settings.UNLIT, Settings.NORMALS, Settings.DEPTH, Settings.SILHOUETTE,
    ]

    def __init__(self):
        super(SettingsWidget, self).__init__()
        # Widget state of main app window and the scene that is controlled by the settings
        self.settings = Settings()
        # self.scene_widget = None
        # layout = QVBoxLayout()
        self.widget = QWidget()

        combobox = QtWidgets.QComboBox()
        combobox.addItems(SettingsWidget.MATERIAL_NAMES)
        combobox.currentIndexChanged.connect(lambda string: print(string))

        layout = QVBoxLayout()
        layout.addWidget(combobox)
        self.widget.setLayout(layout)

        # self._arcball_button = gui.Button("Arcball")
        # self._arcball_button.horizontal_padding_em = 0.5
        # self._arcball_button.vertical_padding_em = 0
        #
        # self._fly_button = gui.Button("Fly")
        # self._fly_button.horizontal_padding_em = 0.5
        # self._fly_button.vertical_padding_em = 0
        # self._model_button = gui.Button("Model")
        # self._model_button.horizontal_padding_em = 0.5
        # self._model_button.vertical_padding_em = 0
        # self._sun_button = gui.Button("Sun")
        # self._sun_button.horizontal_padding_em = 0.5
        # self._sun_button.vertical_padding_em = 0
        # self._ibl_button = gui.Button("Environment")
        # self._ibl_button.horizontal_padding_em = 0.5
        # self._ibl_button.vertical_padding_em = 0
        # view_ctrls.add_child(gui.Label("Mouse controls"))
        # # We want two rows of buttons, so make two horizontal layouts. We also
        # # want the buttons centered, which we can do be putting a stretch item
        # # as the first and last item. Stretch items take up as much space as
        # # possible, and since there are two, they will each take half the extra
        # # space, thus centering the buttons.
        # h = gui.Horiz(0.25 * em)  # row 1
        # h.add_stretch()
        # h.add_child(self._arcball_button)
        # h.add_child(self._fly_button)
        # h.add_child(self._model_button)
        # h.add_stretch()
        # view_ctrls.add_child(h)
        # h = gui.Horiz(0.25 * em)  # row 2
        # h.add_stretch()
        # h.add_child(self._sun_button)
        # h.add_child(self._ibl_button)
        # h.add_stretch()
        # view_ctrls.add_child(h)
        #
        # self._show_skybox = gui.Checkbox("Show skymap")
        # self._show_skybox.set_on_checked(self._on_show_skybox)
        # view_ctrls.add_fixed(separation_height)
        # view_ctrls.add_child(self._show_skybox)
        #
        # self._bg_color = gui.ColorEdit()
        # self._bg_color.set_on_value_changed(self._on_bg_color)
        #
        # grid = gui.VGrid(2, 0.25 * em)
        # grid.add_child(gui.Label("BG Color"))
        # grid.add_child(self._bg_color)
        # view_ctrls.add_child(grid)
        #
        # self._show_axes = gui.Checkbox("Show axes")
        # self._show_axes.set_on_checked(self._on_show_axes)
        # view_ctrls.add_fixed(separation_height)
        # view_ctrls.add_child(self._show_axes)
        #
        # self._profiles = gui.Combobox()
        # # for name in sorted(Settings.LIGHTING_PROFILES.keys()):
        # #     self._profiles.add_item(name)
        # # self._profiles.add_item(Settings.CUSTOM_PROFILE_NAME)
        # view_ctrls.add_fixed(separation_height)
        # view_ctrls.add_child(gui.Label("Lighting profiles"))
        # view_ctrls.add_child(self._profiles)
        # self.widget.add_fixed(separation_height)
        # self.widget.add_child(view_ctrls)
        #
        # self.widget.add_fixed(separation_height)
        #
        # material_settings = gui.CollapsableVert("Material settings", 0,
        #                                         gui.Margins(em, 0, 0, 0))
        #
        # self._shader = gui.Combobox()
        # for material in SettingsWidget.MATERIAL_NAMES:
        #     self._shader.add_item(material)
        #
        # self._shader.set_on_selection_changed(self._on_shader)
        # self._material_prefab = gui.Combobox()
        # for prefab_name in sorted(Settings.PREFAB.keys()):
        #     self._material_prefab.add_item(prefab_name)
        # self._material_prefab.selected_text = Settings.DEFAULT_MATERIAL_NAME
        # self._material_prefab.set_on_selection_changed(self._on_material_prefab)
        # self._material_color = gui.ColorEdit()
        # self._material_color.set_on_value_changed(self._on_material_color)
        # self._point_size = gui.Slider(gui.Slider.INT)
        # self._point_size.set_limits(1, 10)
        # self._point_size.set_on_value_changed(self._on_point_size)
        #
        # grid = gui.VGrid(2, 0.25 * em)
        # grid.add_child(gui.Label("Type"))
        # grid.add_child(self._shader)
        # grid.add_child(gui.Label("Material"))
        # grid.add_child(self._material_prefab)
        # grid.add_child(gui.Label("Color"))
        # grid.add_child(self._material_color)
        # grid.add_child(gui.Label("Point size"))
        # grid.add_child(self._point_size)
        # material_settings.add_child(grid)
        #
        # self.widget.add_fixed(separation_height)
        # self.widget.add_child(material_settings)

    def initialize(self, scene_widget):
        self.scene_widget = scene_widget
        # Button events
        # self._arcball_button.set_on_clicked(self.scene_widget.set_mouse_mode_rotate)
        # self._fly_button.set_on_clicked(self.scene_widget.set_mouse_mode_fly)
        # self._model_button.set_on_clicked(self.scene_widget.set_mouse_mode_model)
        # self._sun_button.set_on_clicked(self.scene_widget.set_mouse_mode_sun)
        # self._ibl_button.set_on_clicked(self.scene_widget.set_mouse_mode_ibl)
    #
    # def _save_state(self):
    #     self._bg_color.color_value = self.settings.bg_color
    #     self._show_axes.checked = self.settings.show_axes
    #     self._material_prefab.enabled = (
    #         self.settings.material.shader == Settings.LIT)
    #     c = gui.Color(self.settings.material.base_color[0],
    #                   self.settings.material.base_color[1],
    #                   self.settings.material.base_color[2],
    #                   self.settings.material.base_color[3])
    #     self._material_color.color_value = c
    #     self._point_size.double_value = self.settings.material.point_size

    def _apply_and_save(self):
        self.scene_widget.apply_settings(self.settings)
        # self._save_state()

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

    def _on_shader(self, _, index):
        self.settings.set_material(SettingsWidget.MATERIAL_SHADERS[index])
        self._apply_and_save()

    def _on_material_prefab(self, name, _):
        self.settings.apply_material_prefab(name)
        self.settings.apply_material = True
        self._apply_and_save()

    def _on_material_color(self, color):
        self.settings.material.base_color = [
            color.red, color.green, color.blue, color.alpha
        ]
        self.settings.apply_material = True
        self._apply_and_save()

    def _on_point_size(self, size):
        self.settings.material.point_size = int(size)
        self.settings.apply_material = True
        self._apply_and_save()

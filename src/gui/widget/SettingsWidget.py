import glob
import os
import open3d.visualization.gui as gui

from src.gui.Settings import Settings
from src.gui.Utils import DEFAULT_IBL


class SettingsWidget:
    MATERIAL_NAMES = ["Lit", "Unlit", "Normals", "Depth", "Silhouette"]
    MATERIAL_SHADERS = [
        Settings.LIT, Settings.UNLIT, Settings.NORMALS, Settings.DEPTH, Settings.SILHOUETTE,
    ]

    def __init__(self, window, update_scene):
        self.settings = Settings()
        resource_path = gui.Application.instance.resource_path
        self.settings.new_ibl_name = resource_path + "/" + DEFAULT_IBL

        # ---- Settings panel ----
        # Rather than specifying sizes in pixels, which may vary in size based
        # on the monitor, especially on macOS which has 220 dpi monitors, use
        # the em-size. This way sizings will be proportional to the font size,
        # which will create a more visually consistent size across platforms.
        em = window.theme.font_size
        separation_height = int(round(0.5 * em))

        # Widgets are laid out in layouts: gui.Horiz, gui.Vert,
        # gui.CollapsableVert, and gui.VGrid. By nesting the layouts we can
        # achieve complex designs. Usually we use a vertical layout as the
        # topmost widget, since widgets tend to be organized from top to bottom.
        # Within that, we usually have a series of horizontal layouts for each
        # row. All layouts take a spacing parameter, which is the spacing
        # between items in the widget, and a margins parameter, which specifies
        # the spacing of the left, top, right, bottom margins. (This acts like
        # the 'padding' property in CSS.)
        self.settings_panel = gui.Vert(
            0, gui.Margins(0.25 * em, 0.25 * em, 0.25 * em, 0.25 * em))

        # Create a collapsable vertical widget, which takes up enough vertical
        # space for all its children when open, but only enough for text when
        # closed. This is useful for property pages, so the user can hide sets
        # of properties they rarely use.
        view_ctrls = gui.CollapsableVert("View controls", 0.25 * em,
                                         gui.Margins(em, 0, 0, 0))

        self.arcball_button = gui.Button("Arcball")
        self.arcball_button.horizontal_padding_em = 0.5
        self.arcball_button.vertical_padding_em = 0
        self.fly_button = gui.Button("Fly")
        self.fly_button.horizontal_padding_em = 0.5
        self.fly_button.vertical_padding_em = 0
        self.model_button = gui.Button("Model")
        self.model_button.horizontal_padding_em = 0.5
        self.model_button.vertical_padding_em = 0
        self.sun_button = gui.Button("Sun")
        self.sun_button.horizontal_padding_em = 0.5
        self.sun_button.vertical_padding_em = 0
        self.ibl_button = gui.Button("Environment")
        self.ibl_button.horizontal_padding_em = 0.5
        self.ibl_button.vertical_padding_em = 0
        view_ctrls.add_child(gui.Label("Mouse controls"))
        # We want two rows of buttons, so make two horizontal layouts. We also
        # want the buttons centered, which we can do be putting a stretch item
        # as the first and last item. Stretch items take up as much space as
        # possible, and since there are two, they will each take half the extra
        # space, thus centering the buttons.
        h = gui.Horiz(0.25 * em)  # row 1
        h.add_stretch()
        h.add_child(self.arcball_button)
        h.add_child(self.fly_button)
        h.add_child(self.model_button)
        h.add_stretch()
        view_ctrls.add_child(h)
        h = gui.Horiz(0.25 * em)  # row 2
        h.add_stretch()
        h.add_child(self.sun_button)
        h.add_child(self.ibl_button)
        h.add_stretch()
        view_ctrls.add_child(h)

        self._show_skybox = gui.Checkbox("Show skymap")
        self._show_skybox.set_on_checked(lambda show: self._on_show_skybox(show, update_scene))
        view_ctrls.add_fixed(separation_height)
        view_ctrls.add_child(self._show_skybox)

        self._bg_color = gui.ColorEdit()
        self._bg_color.set_on_value_changed(lambda color: self._on_bg_color(color, update_scene))

        grid = gui.VGrid(2, 0.25 * em)
        grid.add_child(gui.Label("BG Color"))
        grid.add_child(self._bg_color)
        view_ctrls.add_child(grid)

        self._show_axes = gui.Checkbox("Show axes")
        self._show_axes.set_on_checked(lambda show: self._on_show_axes(show, update_scene))
        view_ctrls.add_fixed(separation_height)
        view_ctrls.add_child(self._show_axes)

        self._profiles = gui.Combobox()
        for name in sorted(Settings.LIGHTING_PROFILES.keys()):
            self._profiles.add_item(name)
        self._profiles.add_item(Settings.CUSTOM_PROFILE_NAME)
        self._profiles.set_on_selection_changed(lambda name, index: self._on_lighting_profile(name, index, update_scene))
        view_ctrls.add_fixed(separation_height)
        view_ctrls.add_child(gui.Label("Lighting profiles"))
        view_ctrls.add_child(self._profiles)
        self.settings_panel.add_fixed(separation_height)
        self.settings_panel.add_child(view_ctrls)

        advanced = gui.CollapsableVert("Advanced lighting", 0,
                                       gui.Margins(em, 0, 0, 0))
        advanced.set_is_open(False)

        self._use_ibl = gui.Checkbox("HDR map")
        self._use_ibl.set_on_checked(lambda use: self._on_use_ibl(use, update_scene))
        self._use_sun = gui.Checkbox("Sun")
        self._use_sun.set_on_checked(lambda use: self._on_use_sun(use, update_scene))
        advanced.add_child(gui.Label("Light sources"))
        h = gui.Horiz(em)
        h.add_child(self._use_ibl)
        h.add_child(self._use_sun)
        advanced.add_child(h)

        self._ibl_map = gui.Combobox()
        for ibl in glob.glob(gui.Application.instance.resource_path + "/*_ibl.ktx"):
            self._ibl_map.add_item(os.path.basename(ibl[:-8]))

        self._ibl_map.selected_text = DEFAULT_IBL
        self._ibl_map.set_on_selection_changed(lambda name, index: self._on_new_ibl(name, index, update_scene))
        self._ibl_intensity = gui.Slider(gui.Slider.INT)
        self._ibl_intensity.set_limits(0, 200000)
        self._ibl_intensity.set_on_value_changed(lambda intensity: self._on_ibl_intensity(intensity, update_scene))
        grid = gui.VGrid(2, 0.25 * em)
        grid.add_child(gui.Label("HDR map"))
        grid.add_child(self._ibl_map)
        grid.add_child(gui.Label("Intensity"))
        grid.add_child(self._ibl_intensity)
        advanced.add_fixed(separation_height)
        advanced.add_child(gui.Label("Environment"))
        advanced.add_child(grid)

        self._sun_intensity = gui.Slider(gui.Slider.INT)
        self._sun_intensity.set_limits(0, 200000)
        self._sun_intensity.set_on_value_changed(lambda intensity: self._on_sun_intensity(intensity, update_scene))
        self._sun_dir = gui.VectorEdit()
        self._sun_dir.set_on_value_changed(lambda sun_dir: self._on_sun_dir(sun_dir, update_scene))
        self._sun_color = gui.ColorEdit()
        self._sun_color.set_on_value_changed(lambda color: self._on_sun_color(color, update_scene))
        grid = gui.VGrid(2, 0.25 * em)
        grid.add_child(gui.Label("Intensity"))
        grid.add_child(self._sun_intensity)
        grid.add_child(gui.Label("Direction"))
        grid.add_child(self._sun_dir)
        grid.add_child(gui.Label("Color"))
        grid.add_child(self._sun_color)
        advanced.add_fixed(separation_height)
        advanced.add_child(gui.Label("Sun (Directional light)"))
        advanced.add_child(grid)

        self.settings_panel.add_fixed(separation_height)
        self.settings_panel.add_child(advanced)

        material_settings = gui.CollapsableVert("Material settings", 0,
                                                gui.Margins(em, 0, 0, 0))

        self._shader = gui.Combobox()
        for material in SettingsWidget.MATERIAL_NAMES:
            self._shader.add_item(material)

        self._shader.set_on_selection_changed(lambda name, index: self._on_shader(name, index, update_scene))
        self._material_prefab = gui.Combobox()
        for prefab_name in sorted(Settings.PREFAB.keys()):
            self._material_prefab.add_item(prefab_name)
        self._material_prefab.selected_text = Settings.DEFAULT_MATERIAL_NAME
        self._material_prefab.set_on_selection_changed(lambda name, index: self._on_material_prefab(name, index, update_scene))
        self._material_color = gui.ColorEdit()
        self._material_color.set_on_value_changed(lambda color: self._on_material_color(color, update_scene))
        self._point_size = gui.Slider(gui.Slider.INT)
        self._point_size.set_limits(1, 10)
        self._point_size.set_on_value_changed(lambda size: self._on_point_size(size, update_scene))

        grid = gui.VGrid(2, 0.25 * em)
        grid.add_child(gui.Label("Type"))
        grid.add_child(self._shader)
        grid.add_child(gui.Label("Material"))
        grid.add_child(self._material_prefab)
        grid.add_child(gui.Label("Color"))
        grid.add_child(self._material_color)
        grid.add_child(gui.Label("Point size"))
        grid.add_child(self._point_size)
        material_settings.add_child(grid)

        self.settings_panel.add_fixed(separation_height)
        self.settings_panel.add_child(material_settings)

    def _save_state(self):
        self._bg_color.color_value = self.settings.bg_color
        self._show_skybox.checked = self.settings.show_skybox
        self._show_axes.checked = self.settings.show_axes
        self._use_ibl.checked = self.settings.use_ibl
        self._use_sun.checked = self.settings.use_sun
        self._ibl_intensity.int_value = self.settings.ibl_intensity
        self._sun_intensity.int_value = self.settings.sun_intensity
        self._sun_dir.vector_value = self.settings.sun_dir
        self._sun_color.color_value = self.settings.sun_color
        self._material_prefab.enabled = (
            self.settings.material.shader == Settings.LIT)
        c = gui.Color(self.settings.material.base_color[0],
                      self.settings.material.base_color[1],
                      self.settings.material.base_color[2],
                      self.settings.material.base_color[3])
        self._material_color.color_value = c
        self._point_size.double_value = self.settings.material.point_size

    def _apply_and_save(self, apply_settings):
        apply_settings()
        self._save_state()

    def _on_bg_color(self, new_color, apply_settings):
        self.settings.bg_color = new_color
        self._apply_and_save(apply_settings)

    def _on_show_skybox(self, show, apply_settings):
        self.settings.show_skybox = show
        self._apply_and_save(apply_settings)

    def _on_show_axes(self, show, apply_settings):
        self.settings.show_axes = show
        self._apply_and_save(apply_settings)

    def _on_use_ibl(self, use, apply_settings):
        self.settings.use_ibl = use
        self._profiles.selected_text = Settings.CUSTOM_PROFILE_NAME
        self._apply_and_save(apply_settings)

    def _on_use_sun(self, use, apply_settings):
        self.settings.use_sun = use
        self._profiles.selected_text = Settings.CUSTOM_PROFILE_NAME
        self._apply_and_save(apply_settings)

    def _on_lighting_profile(self, name, index, apply_settings):
        if name != Settings.CUSTOM_PROFILE_NAME:
            self.settings.apply_lighting_profile(name)
            self._apply_and_save(apply_settings)

    def _on_new_ibl(self, name, index, apply_settings):
        self.settings.new_ibl_name = gui.Application.instance.resource_path + "/" + name
        self._profiles.selected_text = Settings.CUSTOM_PROFILE_NAME
        self._apply_and_save(apply_settings)

    def _on_ibl_intensity(self, intensity, apply_settings):
        self.settings.ibl_intensity = int(intensity)
        self._profiles.selected_text = Settings.CUSTOM_PROFILE_NAME
        self._apply_and_save(apply_settings)

    def _on_sun_intensity(self, intensity, apply_settings):
        self.settings.sun_intensity = int(intensity)
        self._profiles.selected_text = Settings.CUSTOM_PROFILE_NAME
        self._apply_and_save(apply_settings)

    def _on_sun_dir(self, sun_dir, apply_settings):
        self.settings.sun_dir = sun_dir
        self._profiles.selected_text = Settings.CUSTOM_PROFILE_NAME
        self._apply_and_save(apply_settings)

    def _on_sun_color(self, color, apply_settings):
        self.settings.sun_color = color
        self._apply_and_save(apply_settings)

    def _on_shader(self, name, index, apply_settings):
        self.settings.set_material(SettingsWidget.MATERIAL_SHADERS[index])
        self._apply_and_save(apply_settings)

    def _on_material_prefab(self, name, index, apply_settings):
        self.settings.apply_material_prefab(name)
        self.settings.apply_material = True
        self._apply_and_save(apply_settings)

    def _on_material_color(self, color, apply_settings):
        self.settings.material.base_color = [
            color.red, color.green, color.blue, color.alpha
        ]
        self.settings.apply_material = True
        self._apply_and_save(apply_settings)

    def _on_point_size(self, size, apply_settings):
        self.settings.material.point_size = int(size)
        self.settings.apply_material = True
        self._apply_and_save(apply_settings)

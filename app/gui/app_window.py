import open3d.visualization.gui as gui
from app.gui.menu import Menu
from app.gui.widget.scene_widget import SceneWidget
from app.gui.widget.settings_widget import SettingsWidget
from app.gui.widget.properties_widget import PropertiesWidget


class AppWindow:
    def __init__(self, width, height):
        self.window = gui.Application.instance.create_window(
            "Open3D", width, height)

        # Use the em-size. This way sizings will be proportional to the font size
        em = self.window.theme.font_size

        # Menu
        self.Menu = Menu()
        self.settings_widget = SettingsWidget(em, self._update_scene_widget)
        self.scene_widget = SceneWidget(self.window.renderer, lambda dir: self.settings_widget._on_sun_dir(dir, self._update_scene_widget))
        self.properties_widget = PropertiesWidget(em)

        # Set events
        self.set_click_events()
        self.set_menu()

        # Normally our user interface can be children of all one layout (usually
        # a vertical layout), which is then the only child of the window. In our
        # case we want the scene to take up all the space and the settings panel
        # to go above it. We can do this custom layout by providing an on_layout
        # callback. The on_layout callback should set the frame
        # (position + size) of every child correctly. After the callback is
        # done the window will layout the grandchildren.
        self.window.set_on_layout(self._on_layout)
        self.window.add_child(self.scene_widget.widget)
        self.window.add_child(self.settings_widget.settings_panel)
        self.window.add_child(self.properties_widget.widget)

        self._update_scene_widget()

    def set_menu(self):
        # The menubar is global, but we need to connect the menu items to the
        # window, so that the window can call the appropriate function when the
        # menu item is activated.
        self.window.set_on_menu_item_activated(
            Menu.OPEN,
            lambda: self.Menu.on_menu_open(
                self.window,
                lambda path: self.scene_widget.load_shape(
                    path,
                    self.settings_widget.settings.material,
                    lambda features: self.properties_widget.update_properties(features))))
        self.window.set_on_menu_item_activated(Menu.EXPORT, lambda: self.Menu.on_menu_export(self.window, lambda path: self.scene_widget.export_image(path)))
        self.window.set_on_menu_item_activated(Menu.QUIT, lambda: self.Menu.on_menu_quit())
        self.window.set_on_menu_item_activated(Menu.ABOUT, lambda: self.Menu.on_menu_about(self.window))

    def _update_scene_widget(self):
        self.scene_widget.apply_settings(self.settings_widget.settings)

    def set_click_events(self):
        self.settings_widget.arcball_button.set_on_clicked(self.scene_widget.set_mouse_mode_rotate)
        self.settings_widget.fly_button.set_on_clicked(self.scene_widget.set_mouse_mode_fly)
        self.settings_widget.model_button.set_on_clicked(self.scene_widget.set_mouse_mode_model)
        self.settings_widget.sun_button.set_on_clicked(self.scene_widget.set_mouse_mode_sun)
        self.settings_widget.ibl_button.set_on_clicked(self.scene_widget.set_mouse_mode_ibl)

    def _on_layout(self, layout_context):
        # The on_layout callback should set the frame (position + size) of every
        # child correctly. After the callback is done the window will layout
        # the grandchildren.
        r = self.window.content_rect

        width = 17 * layout_context.theme.font_size
        properties_height = min(100, r.height / 2)
        self.settings_widget.settings_panel.frame = gui.Rect(0, r.y, width, r.height - properties_height)
        self.properties_widget.widget.frame = gui.Rect(0, r.height - properties_height, width, r.height)
        self.scene_widget.widget.frame = gui.Rect(width, r.y, r.get_right() - width, r.height)

import open3d.visualization.gui as gui
from src.gui.Menu import Menu
from src.gui.widget.SceneWidget import SceneWidget
from src.gui.widget.SettingsWidget import SettingsWidget


class AppWindow:
    MENU_OPEN = 1
    MENU_EXPORT = 2
    MENU_QUIT = 3
    MENU_SHOW_SETTINGS = 11
    MENU_ABOUT = 21

    def __init__(self, width, height):
        self.window = gui.Application.instance.create_window(
            "Open3D", width, height)
        w = self.window  # to make the code more concise

        # Menu
        self.Menu = Menu(self)
        self.settings_widget = SettingsWidget(w, self._update_scene_widget)
        self.scene_widget = SceneWidget(w, lambda dir: self.settings_widget._on_sun_dir(dir, self._update_scene_widget))

        self.scene_widget2 = SceneWidget(w, lambda dir: self.settings_widget._on_sun_dir(dir, self._update_scene_widget))

        # Set events
        self.set_click_events()
        self.set_menu(w)

        # Normally our user interface can be children of all one layout (usually
        # a vertical layout), which is then the only child of the window. In our
        # case we want the scene to take up all the space and the settings panel
        # to go above it. We can do this custom layout by providing an on_layout
        # callback. The on_layout callback should set the frame
        # (position + size) of every child correctly. After the callback is
        # done the window will layout the grandchildren.
        w.set_on_layout(self._on_layout)
        w.add_child(self.scene_widget.widget)
        w.add_child(self.scene_widget2.widget)
        w.add_child(self.settings_widget.settings_panel)

        self._update_scene_widget()

    def set_menu(self, window):
        # The menubar is global, but we need to connect the menu items to the
        # window, so that the window can call the appropriate function when the
        # menu item is activated.
        window.set_on_menu_item_activated(AppWindow.MENU_OPEN,
                                          lambda: self.Menu.on_menu_open(self.window, lambda path: self.scene_widget.load(path, self.settings_widget.settings.material)))
        window.set_on_menu_item_activated(AppWindow.MENU_EXPORT,
                                          lambda: self.Menu.on_menu_export(self.window, lambda path: self.scene_widget.export_image(path)))
        window.set_on_menu_item_activated(AppWindow.MENU_QUIT,
                                          lambda: self.Menu.on_menu_quit())
        window.set_on_menu_item_activated(AppWindow.MENU_SHOW_SETTINGS,
                                          lambda: self.Menu.on_menu_toggle_settings_panel())
        window.set_on_menu_item_activated(AppWindow.MENU_ABOUT,
                                          lambda: self.Menu.on_menu_about(self.window))

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
        height = min(
            r.height,
            self.settings_widget.settings_panel.calc_preferred_size(
                layout_context, gui.Widget.Constraints()).height)
        self.settings_widget.settings_panel.frame = gui.Rect(0, r.y, width, r.height)
        self.scene_widget.widget.frame = gui.Rect(width, r.y, r.get_right() - width, r.height)

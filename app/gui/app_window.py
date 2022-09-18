import open3d.visualization.gui as gui
from app.gui.menu import Menu
from app.gui.widget.scene_widget import SceneWidget
from app.gui.widget.settings_widget import SettingsWidget
from app.gui.widget.properties_widget import PropertiesWidget


class AppWindow:
    def __init__(self, width, height):
        self.window = gui.Application.instance.create_window("Open3D", width, height)
        self.active_widgets = []

        # Use the em-size. This way sizings will be proportional to the font size
        em = self.window.theme.font_size

        # Widgets
        self.properties_widget = PropertiesWidget(self.active_widgets, em)
        self.scene_widget = SceneWidget(self.active_widgets, self.window.renderer)
        self.settings_widget = SettingsWidget(self.active_widgets, em)

        # Initialize the events of the widgets after they are created
        self.scene_widget.initialize(self.properties_widget, self.settings_widget)
        self.settings_widget.initialize(self.scene_widget)

        # Add to list of widgets
        self.active_widgets.append(self.properties_widget)
        self.active_widgets.append(self.scene_widget)
        self.active_widgets.append(self.settings_widget)

        # Menu
        self.Menu = Menu(self.active_widgets, self.scene_widget)
        self.set_menu()

        # Normally our user interface can be children of all one layout (usually
        # a vertical layout), which is then the only child of the window. In our
        # case we want the scene to take up all the space and the settings panel
        # to go above it. We can do this custom layout by providing an on_layout
        # callback. The on_layout callback should set the frame
        # (position + size) of every child correctly. After the callback is
        # done the window will layout the grandchildren.
        self.window.set_on_layout(self._on_layout)

        # Add all widgets
        for active_widget in self.active_widgets:
            self.window.add_child(active_widget.widget)

        self.scene_widget.apply_settings(self.settings_widget.settings)

    def set_menu(self):
        # The menubar is global, but we need to connect the menu items to the
        # window, so that the window can call the appropriate function when the
        # menu item is activated.
        self.window.set_on_menu_item_activated(Menu.OPEN, lambda: self.Menu.on_menu_open(self.window))
        self.window.set_on_menu_item_activated(Menu.EXPORT, lambda: self.Menu.on_menu_export(self.window))
        self.window.set_on_menu_item_activated(Menu.QUIT, self.Menu.on_menu_quit)
        self.window.set_on_menu_item_activated(Menu.ABOUT, lambda: self.Menu.on_menu_about(self.window))

    def _on_layout(self, layout_context):
        # The on_layout callback should set the frame (position + size) of every
        # child correctly. After the callback is done the window will layout
        # the grandchildren.
        r = self.window.content_rect

        width = 17 * layout_context.theme.font_size
        properties_height = min(100, r.height / 2)
        self.settings_widget.widget.frame = gui.Rect(0, r.y, width, r.height - properties_height)
        self.properties_widget.widget.frame = gui.Rect(0, r.height - properties_height, width, r.height)
        self.scene_widget.widget.frame = gui.Rect(width, r.y, r.get_right() - width, r.height)

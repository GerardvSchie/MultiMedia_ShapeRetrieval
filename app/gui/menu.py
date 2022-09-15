import open3d.visualization.gui as gui

from app.gui.utils import isMacOS


class Menu:
    OPEN = 1
    EXPORT = 2
    QUIT = 3
    ABOUT = 11

    def __init__(self):
        # The menu is global (because the macOS menu is global), so only create
        # it once, no matter how many windows are created
        if gui.Application.instance.menubar is not None:
            return

        if isMacOS:
            app_menu = gui.Menu()
            app_menu.add_item("About", Menu.ABOUT)
            app_menu.add_separator()
            app_menu.add_item("Quit", Menu.QUIT)
        file_menu = gui.Menu()
        file_menu.add_item("Open...", Menu.OPEN)
        file_menu.add_item("Export Current Image...", Menu.EXPORT)
        if not isMacOS:
            file_menu.add_separator()
            file_menu.add_item("Quit", Menu.QUIT)
        help_menu = gui.Menu()
        help_menu.add_item("About", Menu.ABOUT)

        menu = gui.Menu()
        if isMacOS:
            # macOS will name the first menu item for the running application
            # (in our case, probably "Python"), regardless of what we call
            # it. This is the application menu, and it is where the
            # About..., Preferences..., and Quit menu items typically go.
            menu.add_menu("Example", app_menu)
            menu.add_menu("File", file_menu)
            # Don't include help menu unless it has something more than
            # About...
        else:
            menu.add_menu("File", file_menu)
            menu.add_menu("Help", help_menu)
        gui.Application.instance.menubar = menu

    def on_menu_open(self, window, on_success):
        dlg = gui.FileDialog(gui.FileDialog.OPEN, "Choose file to load",
                             window.theme)

        dlg.set_path("data")
        dlg.add_filter(
            ".ply .stl .fbx .obj .off .gltf .glb",
            "Triangle mesh files (.ply, .stl, .fbx, .obj, .off, "
            ".gltf, .glb)")
        dlg.add_filter(
            ".xyz .xyzn .xyzrgb .ply .pcd .pts",
            "Point cloud files (.xyz, .xyzn, .xyzrgb, .ply, "
            ".pcd, .pts)")
        dlg.add_filter(".ply", "Polygon files (.ply)")
        dlg.add_filter(".stl", "Stereolithography files (.stl)")
        dlg.add_filter(".fbx", "Autodesk Filmbox files (.fbx)")
        dlg.add_filter(".obj", "Wavefront OBJ files (.obj)")
        dlg.add_filter(".off", "Object file format (.off)")
        dlg.add_filter(".gltf", "OpenGL transfer files (.gltf)")
        dlg.add_filter(".glb", "OpenGL binary transfer files (.glb)")
        dlg.add_filter(".xyz", "ASCII point cloud files (.xyz)")
        dlg.add_filter(".xyzn", "ASCII point cloud with normals (.xyzn)")
        dlg.add_filter(".xyzrgb",
                       "ASCII point cloud files with colors (.xyzrgb)")
        dlg.add_filter(".pcd", "Point Cloud Data files (.pcd)")
        dlg.add_filter(".pts", "3D Points files (.pts)")
        dlg.add_filter("", "All files")

        # A file dialog MUST define on_cancel and on_done functions
        dlg.set_on_cancel(window.close_dialog)
        dlg.set_on_done(lambda filename: self._on_load_dialog_done(window, filename, on_success))
        window.show_dialog(dlg)

    @staticmethod
    def _on_load_dialog_done(window, filename, on_success):
        window.close_dialog()
        on_success(filename)

    def on_menu_export(self, window, on_success):
        dlg = gui.FileDialog(gui.FileDialog.SAVE, "Choose file to save",
                             window.theme)
        dlg.add_filter(".png", "PNG files (.png)")
        dlg.set_on_cancel(window.close_dialog)
        dlg.set_on_done(lambda filename: self._on_export_dialog_done(window, filename, on_success))
        window.show_dialog(dlg)

    @staticmethod
    def _on_export_dialog_done(window, filename, on_success):
        window.close_dialog()
        on_success(filename)

    @staticmethod
    def on_menu_quit():
        gui.Application.instance.quit()

    def on_menu_about(self, window):
        # Show a simple dialog. Although the Dialog is actually a widget, you can
        # treat it similar to a Window for layout and put all the widgets in a
        # layout which you make the only child of the Dialog.
        em = window.theme.font_size
        dlg = gui.Dialog("About")

        # Add the text
        dlg_layout = gui.Vert(em, gui.Margins(em, em, em, em))
        dlg_layout.add_child(gui.Label("Open3D GUI Example"))

        # Add the Ok button. We need to define a callback function to handle
        # the click.
        ok = gui.Button("OK")
        ok.set_on_clicked(window.close_dialog)

        # We want the Ok button to be an the right side, so we need to add
        # a stretch item to the layout, otherwise the button will be the size
        # of the entire row. A stretch item takes up as much space as it can,
        # which forces the button to be its minimum size.
        h = gui.Horiz()
        h.add_stretch()
        h.add_child(ok)
        h.add_stretch()
        dlg_layout.add_child(h)

        dlg.add_child(dlg_layout)
        window.show_dialog(dlg)

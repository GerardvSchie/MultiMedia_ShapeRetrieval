import open3d.visualization.gui as gui
import open3d.visualization.rendering as rendering
import numpy as np
import open3d as o3d


class SceneWidget:
    def __init__(self, window, on_sun_dir):
        # 3D widget
        self.widget = gui.SceneWidget()
        self.widget.scene = rendering.Open3DScene(window.renderer)

        # Set camera mode to arc-ball
        # self.widget.set_view_controls(gui.SceneWidget.Controls.ROTATE_CAMERA)
        self.widget.set_on_sun_direction_changed(on_sun_dir)

    def apply_settings(self, settings):
        bg_color = [
            settings.bg_color.red, settings.bg_color.green,
            settings.bg_color.blue, settings.bg_color.alpha
        ]
        self.widget.scene.set_background(bg_color)
        self.widget.scene.show_skybox(settings.show_skybox)
        self.widget.scene.show_axes(settings.show_axes)
        if settings.new_ibl_name is not None:
            self.widget.scene.scene.set_indirect_light(
                settings.new_ibl_name)
            # Clear new_ibl_name, so we don't keep reloading this image every
            # time the settings are applied.
            settings.new_ibl_name = None
        self.widget.scene.scene.enable_indirect_light(settings.use_ibl)
        self.widget.scene.scene.set_indirect_light_intensity(
            settings.ibl_intensity)
        sun_color = [
            settings.sun_color.red, settings.sun_color.green,
            settings.sun_color.blue
        ]
        self.widget.scene.scene.set_sun_light(settings.sun_dir, sun_color,
                                              settings.sun_intensity)
        self.widget.scene.scene.enable_sun_light(settings.use_sun)

        if settings.apply_material:
            self.widget.scene.update_material(settings.material)
            settings.apply_material = False

    # Part of the scene, what is in the window
    def load(self, path, material):
        self.widget.scene.clear_geometry()

        geometry = None
        geometry_type = o3d.io.read_file_geometry_type(path)

        mesh = None
        if geometry_type & o3d.io.CONTAINS_TRIANGLES:
            mesh = o3d.io.read_triangle_mesh(path)
        if mesh is not None:
            if len(mesh.triangles) == 0:
                print(
                    "[WARNING] Contains 0 triangles, will read as point cloud")
                mesh = None
            else:
                mesh.compute_vertex_normals()
                if len(mesh.vertex_colors) == 0:
                    mesh.paint_uniform_color([1, 1, 1])
                geometry = mesh
            # Make sure the mesh has texture coordinates
            if not mesh.has_triangle_uvs():
                uv = np.array([[0.0, 0.0]] * (3 * len(mesh.triangles)))
                mesh.triangle_uvs = o3d.utility.Vector2dVector(uv)
        else:
            print("[Info]", path, "appears to be a point cloud")

        if geometry is None:
            cloud = None
            try:
                cloud = o3d.io.read_point_cloud(path)
            except Exception:
                pass
            if cloud is not None:
                print("[Info] Successfully read", path)
                if not cloud.has_normals():
                    cloud.estimate_normals()
                cloud.normalize_normals()
                geometry = cloud
            else:
                print("[WARNING] Failed to read points", path)

        if geometry is not None:
            try:
                self.widget.scene.add_geometry("__model__", geometry, material)
                bounds = geometry.get_axis_aligned_bounding_box()
                self.widget.setup_camera(60, bounds, bounds.get_center())
            except Exception as e:
                print(e)

    def export_image(self, path):
        def on_image(image):
            img = image

            quality = 9  # png
            if path.endswith(".jpg"):
                quality = 100
            o3d.io.write_image(path, img, quality)

        # frame = self._scene.frame
        # self.export_image(filename, frame.width, frame.height)
        self.widget.scene.scene.render_to_image(on_image)

    def set_mouse_mode_rotate(self):
        self.widget.set_view_controls(gui.SceneWidget.Controls.ROTATE_CAMERA)

    def set_mouse_mode_fly(self):
        self.widget.set_view_controls(gui.SceneWidget.Controls.FLY)

    def set_mouse_mode_sun(self):
        self.widget.set_view_controls(gui.SceneWidget.Controls.ROTATE_SUN)

    def set_mouse_mode_ibl(self):
        self.widget.set_view_controls(gui.SceneWidget.Controls.ROTATE_IBL)

    def set_mouse_mode_model(self):
        self.widget.set_view_controls(gui.SceneWidget.Controls.ROTATE_MODEL)

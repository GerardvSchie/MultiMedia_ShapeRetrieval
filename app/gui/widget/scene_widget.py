import open3d.visualization.gui as gui
import open3d.visualization.rendering as rendering
import open3d as o3d
import logging

from src.object.shape import Shape
from src.pipeline.feature_extractor import FeatureExtractor


# 3D scene widget
class SceneWidget:
    def __init__(self, renderer, on_sun_dir):
        self.widget = gui.SceneWidget()
        self.widget.scene = rendering.Open3DScene(renderer)
        self.shape = None

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
    def load_shape(self, path, material, on_success):
        self.widget.scene.clear_geometry()
        self.shape = Shape(path)

        if self.shape.mesh is None:
            logging.error("Mesh was not loaded successfully")
            return

        FeatureExtractor.extract_features(self.shape)

        if self.shape.geometry is not None:
            try:
                self.widget.scene.add_geometry("__model__", self.shape.geometry, material)
                bounds = self.shape.geometry.get_axis_aligned_bounding_box()
                self.widget.setup_camera(60, bounds, bounds.get_center())
                on_success(self.shape.features)
            except Exception as e:
                logging.error(f"Loading of shape failed with message: {e}")

    def export_image(self, path):
        def on_image(image):
            img = image

            quality = 9  # png
            if path.endswith(".jpg"):
                quality = 100
            o3d.io.write_image(path, img, quality)

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

import open3d.visualization.gui as gui

from src.object.render_mode import RenderMode
from src.object.material_record import MaterialRecord


class Settings:
    DEFAULT_MATERIAL_NAME = "Polished ceramic [default]"
    PREFAB = {
        DEFAULT_MATERIAL_NAME: {
            "metallic": 0.0,
            "roughness": 0.7,
            "reflectance": 0.5,
            "clearcoat": 0.2,
            "clearcoat_roughness": 0.2,
            "anisotropy": 0.0
        },
        "Metal (rougher)": {
            "metallic": 1.0,
            "roughness": 0.5,
            "reflectance": 0.9,
            "clearcoat": 0.0,
            "clearcoat_roughness": 0.0,
            "anisotropy": 0.0
        },
        "Metal (smoother)": {
            "metallic": 1.0,
            "roughness": 0.3,
            "reflectance": 0.9,
            "clearcoat": 0.0,
            "clearcoat_roughness": 0.0,
            "anisotropy": 0.0
        },
        "Plastic": {
            "metallic": 0.0,
            "roughness": 0.5,
            "reflectance": 0.5,
            "clearcoat": 0.5,
            "clearcoat_roughness": 0.2,
            "anisotropy": 0.0
        },
        "Glazed ceramic": {
            "metallic": 0.0,
            "roughness": 0.5,
            "reflectance": 0.9,
            "clearcoat": 1.0,
            "clearcoat_roughness": 0.1,
            "anisotropy": 0.0
        },
        "Clay": {
            "metallic": 0.0,
            "roughness": 1.0,
            "reflectance": 0.5,
            "clearcoat": 0.1,
            "clearcoat_roughness": 0.287,
            "anisotropy": 0.0
        },
    }

    def __init__(self):
        self.mouse_model = gui.SceneWidget.Controls.ROTATE_CAMERA
        self.bg_color = gui.Color(1, 1, 1)
        self.show_axes = False
        self.sun_color = gui.Color(1, 1, 1)

        self.apply_material = True  # clear to False after processing
        self.material_record = MaterialRecord()
        self.render_mode = RenderMode.LIT

    def set_render_mode(self, name):
        self.render_mode = name

        if name == "Unlit":
            self.material_record.set_material(MaterialRecord.UNLIT)
            self.apply_material = True
        elif name == "Lit":
            self.material_record.set_material(MaterialRecord.LIT)
            self.apply_material = True
        elif name == "Normals":
            self.material_record.set_material(MaterialRecord.NORMALS)
            self.apply_material = True
        elif name == "Depth":
            self.material_record.set_material(MaterialRecord.DEPTH)
            self.apply_material = True

    def apply_material_prefab(self, name):
        assert (self.render_mode.shader == MaterialRecord.LIT)
        prefab = Settings.PREFAB[name]
        for key, val in prefab.items():
            setattr(self.render_mode, "base_" + key, val)

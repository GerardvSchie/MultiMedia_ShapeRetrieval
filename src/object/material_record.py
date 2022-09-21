import open3d.visualization.rendering as rendering


class MaterialRecord:
    UNLIT = "defaultUnlit"
    LIT = "defaultLit"
    NORMALS = "normals"
    DEPTH = "depth"

    ALL = [UNLIT, LIT, NORMALS, DEPTH]

    def __init__(self):
        self._material = {
            MaterialRecord.LIT: rendering.MaterialRecord(),
            MaterialRecord.UNLIT: rendering.MaterialRecord(),
            MaterialRecord.NORMALS: rendering.MaterialRecord(),
            MaterialRecord.DEPTH: rendering.MaterialRecord(),
        }

        self._material[MaterialRecord.LIT].base_color = [0.9, 0.9, 0.9, 1.0]
        self._material[MaterialRecord.LIT].shader = MaterialRecord.LIT
        self._material[MaterialRecord.UNLIT].base_color = [0.0, 0.0, 0.0, 0.0]
        self._material[MaterialRecord.UNLIT].shader = MaterialRecord.UNLIT
        self._material[MaterialRecord.NORMALS].shader = MaterialRecord.NORMALS
        self._material[MaterialRecord.DEPTH].shader = MaterialRecord.DEPTH

        self.current_material_name = None
        self.material = None

        # Default material
        self.set_material(MaterialRecord.LIT)

    def set_material(self, name):
        self.current_material_name = name
        self.material = self._material[self.current_material_name]
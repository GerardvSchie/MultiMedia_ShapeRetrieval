import open3d.visualization.gui as gui
from src.object.features import Features


class PropertiesWidget:
    PADDING = 16

    def __init__(self, em):
        # Default values (_class text has spaces because widget width is not recalculated)
        self._class = gui.Label(f"{'-': <{PropertiesWidget.PADDING}}")
        self._nr_vertices = gui.Label("0")
        self._nr_faces = gui.Label("0")
        self._type_faces = gui.Label("-")
        self._axis_aligned_bounding_box = gui.Label("-")

        self.widget = gui.Vert(0, gui.Margins(em, 0, 0, 0))
        self.widget.add_child(gui.Label("Properties"))
        self.grid = gui.VGrid(2, 0.25 * em)
        self._fill_grid()

        self.widget.add_child(self.grid)

    def _fill_grid(self):
        self.grid.add_child(gui.Label("Class:"))
        self.grid.add_child(self._class)
        self.grid.add_child(gui.Label("#Vertices:"))
        self.grid.add_child(self._nr_vertices)
        self.grid.add_child(gui.Label("#Faces:"))
        self.grid.add_child(self._nr_faces)
        self.grid.add_child(gui.Label("Type of faces:"))
        self.grid.add_child(self._type_faces)
        self.grid.add_child(gui.Label("Bounding box:"))
        self.grid.add_child(self._axis_aligned_bounding_box)

    def update_properties(self, features: Features):
        self._class.text = f"{f'{features.true_class}': <{PropertiesWidget.PADDING}}"
        self._nr_vertices.text = str(features.nr_vertices)
        self._nr_faces.text = str(features.nr_faces)
        self._type_faces = str(features.type_faces)
        self._axis_aligned_bounding_box = str(features.axis_aligned_bounding_box)

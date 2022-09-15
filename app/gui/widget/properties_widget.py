import open3d.visualization.gui as gui
from src.object.features import Features


class PropertiesWidget:
    PADDING = 16

    def __init__(self, em):
        # Default values (_class text has spaces because widget width is not recalculated)
        self._class = gui.Label(f"{'-': <{PropertiesWidget.PADDING}}")
        self._nr_vertices = gui.Label("0")
        self._nr_triangles = gui.Label("0")

        self.widget = gui.Vert(0, gui.Margins(em, 0, 0, 0))
        self.widget.add_child(gui.Label("Properties"))
        self.grid = gui.VGrid(2, 0.25 * em)
        self.grid.add_child(gui.Label("Class:"))
        self.grid.add_child(self._class)
        self.grid.add_child(gui.Label("#Vertices:"))
        self.grid.add_child(self._nr_vertices)
        self.grid.add_child(gui.Label("#Triangles"))
        self.grid.add_child(self._nr_triangles)
        self.widget.add_child(self.grid)

    def update_properties(self, features: Features):
        self._class.text = f"{'unknown': <{PropertiesWidget.PADDING}}"
        self._nr_vertices.text = str(features.nr_vertices)
        self._nr_triangles.text = str(features.nr_triangles)

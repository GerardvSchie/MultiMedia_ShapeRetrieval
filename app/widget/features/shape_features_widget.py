from app.widget.util import color_widget
from src.object.features.shape_features import ShapeFeatures

from PyQt6.QtWidgets import QWidget, QLabel

from app.layout.grid_layout import GridLayout


class ShapeFeaturesWidget(QWidget):
    def __init__(self):
        super(ShapeFeaturesWidget, self).__init__()
        color_widget(self, [255, 255, 0])
        self.setFixedWidth(190)

        self.class_value_label = QLabel("-")

        self.mesh_nr_vertices_value_label = QLabel("0")
        self.mesh_nr_faces_value_label = QLabel("0")
        self.mesh_surface_area_value_label = QLabel("0")
        self.mesh_volume_value_label = QLabel("0")

        self.convex_hull_nr_vertices_value_label = QLabel("0")
        self.convex_hull_nr_faces_value_label = QLabel("0")
        self.convex_hull_surface_area_value_label = QLabel("0")
        self.convex_hull_volume_value_label = QLabel("0")

        # Create layout
        layout: GridLayout = GridLayout()
        layout.add_header("Properties")
        layout.add_row("Class:", [self.class_value_label])
        layout.add_section("Mesh")
        layout.add_row("Nr. Vertices:", [self.mesh_nr_vertices_value_label])
        layout.add_row("Nr. Faces:", [self.mesh_nr_faces_value_label])
        layout.add_row("Area:", [self.mesh_surface_area_value_label])
        layout.add_row("Volume:", [self.mesh_volume_value_label])
        layout.add_section("Convex Hull")
        layout.add_row("Nr. Vertices:", [self.convex_hull_nr_vertices_value_label])
        layout.add_row("Nr. Faces:", [self.convex_hull_nr_faces_value_label])
        layout.add_row("Area:", [self.convex_hull_surface_area_value_label])
        layout.add_row("Volume:", [self.convex_hull_volume_value_label])
        self.setLayout(layout)

    def update_widget(self, features: ShapeFeatures):
        self.class_value_label.setText(features.true_class)

        self.mesh_nr_vertices_value_label.setText('{0}'.format(features.mesh_features.nr_vertices))
        self.mesh_nr_faces_value_label.setText('{0}'.format(features.mesh_features.nr_faces))
        self.mesh_surface_area_value_label.setText('{0:.6}'.format(features.mesh_features.surface_area))
        self.mesh_volume_value_label.setText('{0:.6}'.format(features.mesh_features.volume))

        self.convex_hull_nr_vertices_value_label.setText('{0}'.format(features.convex_hull_features.nr_vertices))
        self.convex_hull_nr_faces_value_label.setText('{0}'.format(features.convex_hull_features.nr_faces))
        self.convex_hull_surface_area_value_label.setText('{0:.6}'.format(features.convex_hull_features.surface_area))
        self.convex_hull_volume_value_label.setText('{0:.6}'.format(features.convex_hull_features.volume))

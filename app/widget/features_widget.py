from app.widget.util import color_widget
from src.object.features import Features

from PyQt6.QtWidgets import QWidget, QLabel

from app.layout.grid_layout import GridLayout


class FeaturesWidget(QWidget):
    def __init__(self):
        super(FeaturesWidget, self).__init__()
        color_widget(self, [255, 255, 0])
        self.setFixedWidth(165)

        self.class_value_label = QLabel("-")
        self.nr_vertices_value_label = QLabel("0")
        self.nr_faces_value_label = QLabel("0")
        self.type_faces_value_label = QLabel("-")
        self.mesh_area_value_label = QLabel("0")
        self.convex_hull_area_value_label = QLabel("0")
        self.bounding_box_area_value_label = QLabel("0")

        # Create layout
        layout: GridLayout = GridLayout()
        layout.add_header("Properties")
        layout.add_row("Class:", [self.class_value_label])
        layout.add_row("Nr. Vertices:", [self.nr_vertices_value_label])
        layout.add_row("Nr. Faces:", [self.nr_faces_value_label])
        layout.add_row("Faces type:", [self.type_faces_value_label])
        layout.add_section("Surface area")
        layout.add_row("Mesh:", [self.mesh_area_value_label])
        layout.add_row("Convex hull:", [self.convex_hull_area_value_label])
        layout.add_row("Box:", [self.bounding_box_area_value_label])
        self.setLayout(layout)

    def update_widget(self, features: Features):
        self.class_value_label.setText(features.true_class)
        self.nr_vertices_value_label.setText('{0}'.format(features.nr_vertices))
        self.nr_faces_value_label.setText('{0}'.format(features.nr_faces))
        self.type_faces_value_label.setText(features.type_faces)
        self.mesh_area_value_label.setText('{0:.6}'.format(features.mesh_area))
        self.convex_hull_area_value_label.setText('{0:.6}'.format(features.convex_hull_area))
        self.bounding_box_area_value_label.setText('{0:.6}'.format(features.bounding_box_area))

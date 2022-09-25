from app.widget.util import color_widget
from app.util.font import BOLD_FONT
from src.object.features import Features

from PyQt6.QtWidgets import QGridLayout, QWidget, QLabel
from PyQt6.QtCore import Qt

from app.layout.grid_layout import GridLayout


class FeaturesWidget(QWidget):
    def __init__(self):
        super(FeaturesWidget, self).__init__()
        color_widget(self, [255, 255, 0])

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
        layout.add_row("Class:", self.class_value_label)
        layout.add_row("Nr. Vertices:", self.nr_vertices_value_label)
        layout.add_row("Nr. Faces:", self.nr_faces_value_label)
        layout.add_row("Faces type:", self.type_faces_value_label)
        layout.add_section("Surface area")
        layout.add_row("Mesh:", self.mesh_area_value_label)
        layout.add_row("Convex hull:", self.convex_hull_area_value_label)
        layout.add_row("Box:", self.bounding_box_area_value_label)
        self.setLayout(layout)

    def update_values(self, features: Features):
        self.class_value_label.setText(features.true_class)
        self.nr_vertices_value_label.setText(str(features.nr_vertices))
        self.nr_faces_value_label.setText(str(features.nr_faces))
        self.type_faces_value_label.setText(features.type_faces)
        self.mesh_area_value_label.setText(str(features.mesh_area))
        self.convex_hull_area_value_label.setText(str(features.convex_hull_area))
        self.bounding_box_area_value_label.setText(str(features.bounding_box_area))


#
# class FeaturesWidget(QWidget):
#     def __init__(self):
#         super(FeaturesWidget, self).__init__()
#         color_widget(self, [255, 255, 0])
#
#         # Header label
#         header_label = QLabel("Properties")
#         header_label.setFont(BOLD_FONT)
#         header_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
#
#         # Class tag
#         class_label = QLabel("Class:")
#         self.class_value_label = QLabel("-")
#
#         # Nr vertices
#         nr_vertices_label = QLabel("Nr. Vertices:")
#         self.nr_vertices_value_label = QLabel("0")
#
#         # Nr faces
#         nr_faces_label = QLabel("Nr. Faces:")
#         self.nr_faces_value_label = QLabel("0")
#
#         # Faces type
#         type_faces_label = QLabel('Faces type:')
#         self.type_faces_value_label = QLabel("-")
#
#         # Areas
#         mesh_area_label = QLabel('Mesh area:')
#         self.mesh_area_value_label = QLabel("0")
#         convex_hull_area_label = QLabel('Convex hull area:')
#         self.convex_hull_area_value_label = QLabel("0")
#         bounding_box_area_label = QLabel('Bounding box area:')
#         self.bounding_box_area_value_label = QLabel("0")
#
#         # Create layout
#         layout: QGridLayout = QGridLayout()
#         layout.setAlignment(Qt.AlignmentFlag.AlignTop)
#         layout.addWidget(header_label, 0, 0, 1, -1)
#         layout.addWidget(class_label, 1, 0)
#         layout.addWidget(self.class_value_label, 1, 1)
#         layout.addWidget(nr_vertices_label, 2, 0)
#         layout.addWidget(self.nr_vertices_value_label, 2, 1)
#         layout.addWidget(nr_faces_label, 3, 0)
#         layout.addWidget(self.nr_faces_value_label, 3, 1)
#         layout.addWidget(type_faces_label, 4, 0)
#         layout.addWidget(self.type_faces_value_label, 4, 1)
#
#         # Surface areas
#         surface_area_row = 5
#
#         layout.addWidget(mesh_area_label, 5, 0)
#         layout.addWidget(self.mesh_area_value_label, 5, 1)
#         layout.addWidget(convex_hull_area_label, 6, 0)
#         layout.addWidget(self.convex_hull_area_value_label, 6, 1)
#         layout.addWidget(bounding_box_area_label, 7, 0)
#         layout.addWidget(self.bounding_box_area_value_label, 7, 1)
#
#         self.setLayout(layout)
#
#     def update_values(self, features: Features):
#         self.class_value_label.setText(features.true_class)
#         self.nr_vertices_value_label.setText(str(features.nr_vertices))
#         self.nr_faces_value_label.setText(str(features.nr_faces))
#         self.type_faces_value_label.setText(features.type_faces)
#         self.mesh_area_value_label.setText(str(features.mesh_area))
#         self.convex_hull_area_value_label.setText(str(features.convex_hull_area))
#         self.bounding_box_area_value_label.setText(str(features.bounding_box_area))

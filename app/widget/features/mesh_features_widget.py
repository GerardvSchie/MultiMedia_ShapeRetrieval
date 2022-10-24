from app.widget.util import color_widget
from src.object.features.mesh_features import MeshFeatures

from PyQt6.QtWidgets import QWidget, QLabel

from app.layout.grid_layout import GridLayout


class MeshFeaturesWidget(QWidget):
    def __init__(self):
        super(MeshFeaturesWidget, self).__init__()
        color_widget(self, [122, 122, 122])
        self.setMaximumHeight(160)

        self.nr_vertices_value_label = QLabel("0")
        self.nr_faces_value_label = QLabel("0")
        self.surface_area_value_label = QLabel("0")
        self.volume_value_label = QLabel("0")

        # Create layout
        layout: GridLayout = GridLayout()
        layout.add_row("Nr. Vertices:", [self.nr_vertices_value_label])
        layout.add_row("Nr. Faces:", [self.nr_faces_value_label])
        layout.add_row("Area:", [self.surface_area_value_label])
        layout.add_row("Volume:", [self.volume_value_label])
        self.setLayout(layout)

    def update_widget(self, mesh_features: MeshFeatures):
        self.nr_vertices_value_label.setText('{0}'.format(mesh_features.nr_vertices))
        self.nr_faces_value_label.setText('{0}'.format(mesh_features.nr_faces))
        self.surface_area_value_label.setText('{0:.6}'.format(mesh_features.surface_area))
        self.volume_value_label.setText('{0:.6}'.format(mesh_features.volume))

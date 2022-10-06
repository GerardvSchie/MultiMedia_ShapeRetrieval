from app.widget.util import color_widget
from src.object.features.bounding_box_features import BoundingBoxFeatures

from PyQt6.QtWidgets import QWidget, QLabel

from app.layout.grid_layout import GridLayout


class BoundingBoxFeaturesWidget(QWidget):
    def __init__(self):
        super(BoundingBoxFeaturesWidget, self).__init__()
        color_widget(self, [255, 0, 60])
        self.setMaximumHeight(130)

        self.bounds_value_label = QLabel("0")
        self.surface_area_value_label = QLabel("0")
        self.volume_value_label = QLabel("0")
        self.diameter_value_label = QLabel("0")

        # Create layout
        layout: GridLayout = GridLayout()
        layout.add_header("Bounding box properties")
        layout.add_row("Points:", [self.bounds_value_label])
        layout.add_row("Surface area:", [self.surface_area_value_label])
        layout.add_row("Volume:", [self.volume_value_label])
        layout.add_row("Diameter:", [self.diameter_value_label])
        self.setLayout(layout)

    def update_widget(self, bounding_box_features: BoundingBoxFeatures):
        self.bounds_value_label.setText('p0:({0[0]:.3}, {0[1]:.3}, {0[2]:.3})\np1:({1[0]:.3}, {1[1]:.3}, {1[2]:.3})'.format(bounding_box_features.min_bound, bounding_box_features.max_bound))
        self.surface_area_value_label.setText('{0:.6}'.format(bounding_box_features.surface_area))
        self.volume_value_label.setText('{0:.6}'.format(bounding_box_features.volume))
        self.diameter_value_label.setText('{0:.6}'.format(bounding_box_features.diameter))

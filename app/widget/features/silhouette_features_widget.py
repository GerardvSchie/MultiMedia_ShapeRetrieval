from PyQt6.QtWidgets import QWidget, QLabel

from src.object.features.silhouette_features import SilhouetteFeatures
from app.widget.util import color_widget
from app.layout.grid_layout import GridLayout


class SilhouetteFeaturesWidget(QWidget):
    def __init__(self):
        super(SilhouetteFeaturesWidget, self).__init__()
        color_widget(self, [122, 0, 0])

        self.area_value_label = QLabel("0")
        self.perimeter_value_label = QLabel("0")
        self.compactness_value_label = QLabel("0")
        self.axis_aligned_bounding_box_value_label = QLabel("-")
        self.rectangularity_value_label = QLabel("0")
        self.diameter_value_label = QLabel("0")
        self.eccentricity_value_label = QLabel("0")

        # Create layout
        layout: GridLayout = GridLayout()
        layout.add_row("Area:", [self.area_value_label])
        layout.add_row("Perimeter:", [self.perimeter_value_label])
        layout.add_row("Compactness:", [self.compactness_value_label])
        layout.add_row("AABB:", [self.axis_aligned_bounding_box_value_label])
        layout.add_row("Rectangularity:", [self.rectangularity_value_label])
        layout.add_row("diameter:", [self.diameter_value_label])
        layout.add_row("eccentricity:", [self.eccentricity_value_label])
        self.setLayout(layout)

    def update_widget(self, silhouette_features: SilhouetteFeatures):
        self.area_value_label.setText('{0}'.format(silhouette_features.area))
        self.perimeter_value_label.setText('{0:.6}'.format(silhouette_features.perimeter))
        self.compactness_value_label.setText('{0:.6}'.format(silhouette_features.compactness))
        # self.axis_aligned_bounding_box_value_label.setText('{0:.6}'.format(silhouette_features.axis_aligned_bounding_box))
        self.rectangularity_value_label.setText('{0:.6}'.format(silhouette_features.rectangularity))
        self.diameter_value_label.setText('{0:.6}'.format(silhouette_features.diameter))
        self.eccentricity_value_label.setText('{0:.6}'.format(silhouette_features.eccentricity))

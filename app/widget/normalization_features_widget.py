from app.widget.util import color_widget
from src.object.normalization_features import NormalizationFeatures

from PyQt6.QtWidgets import QWidget, QLabel

from app.layout.grid_layout import GridLayout


class NormalizationFeaturesWidget(QWidget):
    def __init__(self):
        super(NormalizationFeaturesWidget, self).__init__()
        color_widget(self, [255, 0, 255])
        self.setFixedWidth(165)

        self.distance_to_center_label = QLabel("0")
        self.scale_value_label = QLabel("0")
        self.alignment_value_label = QLabel("0")
        self.rotation_value_label = QLabel("0")
        self.flip_value_label = QLabel("0")

        # Create layout
        layout: GridLayout = GridLayout()
        layout.add_header("Normalization properties")
        layout.add_row("Center distance:", [self.distance_to_center_label])
        layout.add_row("Scale:", [self.scale_value_label])
        layout.add_row("Alignment:", [self.alignment_value_label])
        layout.add_row("Rotation:", [self.rotation_value_label])
        layout.add_row("Flip:", [self.flip_value_label])
        self.setLayout(layout)

    def update_widget(self, normalization_features: NormalizationFeatures):
        self.distance_to_center_label.setText('{0:.6}'.format(normalization_features.distance_to_center))
        self.scale_value_label.setText('{0:.6}'.format(normalization_features.scale))
        self.alignment_value_label.setText('{0:.6}'.format(normalization_features.alignment))
        self.rotation_value_label.setText('{0:.6}'.format(normalization_features.rotation))
        self.flip_value_label.setText('{0:.6}'.format(normalization_features.flip))

from PyQt6.QtWidgets import QWidget, QLabel

from src.object.descriptors import Descriptors
from app.widget.util import color_widget
from app.layout.grid_layout import GridLayout


class DescriptorsWidget(QWidget):
    def __init__(self):
        """Widget containing descriptor information about the shape"""
        super(DescriptorsWidget, self).__init__()
        color_widget(self, [180, 50, 122])
        self.setMaximumHeight(130)

        self.surface_area_value_label = QLabel("0")
        self.compactness_value_label = QLabel("0")
        self.rectangularity_value_label = QLabel("0")
        self.diameter_value_label = QLabel("0")
        self.eccentricity_value_label = QLabel("0")

        # Create layout
        layout: GridLayout = GridLayout()
        layout.add_header("Mesh descriptors")
        layout.add_row("Surface area:", [self.surface_area_value_label])
        layout.add_row("Compactness:", [self.compactness_value_label])
        layout.add_row("Rectangularity:", [self.rectangularity_value_label])
        layout.add_row("Diameter:", [self.diameter_value_label])
        layout.add_row("Eccentricity:", [self.eccentricity_value_label])
        self.setLayout(layout)

    def update_widget(self, descriptors: Descriptors) -> None:
        """Update widget with new descriptor data

        :param descriptors: Descriptors data
        """
        self.surface_area_value_label.setText('{0:.6}'.format(descriptors.surface_area))
        self.compactness_value_label.setText('{0:.6}'.format(descriptors.compactness))
        self.rectangularity_value_label.setText('{0:.6}'.format(descriptors.rectangularity))
        self.diameter_value_label.setText('{0:.6}'.format(descriptors.diameter))
        self.eccentricity_value_label.setText('{0:.6}'.format(descriptors.eccentricity))

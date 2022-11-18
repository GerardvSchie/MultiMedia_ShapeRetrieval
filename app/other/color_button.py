import logging

from PyQt6.QtGui import QColor
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QPushButton, QColorDialog


# Source: https://www.pythonguis.com/widgets/qcolorbutton-a-color-selector-tool-for-pyqt/
# Source: https://zetcode.com/pyqt6/dialogs/
class ColorButton(QPushButton):
    """
    Custom Qt Widget to show a chosen color.

    Left-clicking the button shows the color-chooser, while
    right-clicking resets the color to None (no-color).
    """
    def __init__(self, mesh_color_button: bool, *args, **kwargs):
        """Creates pushbutton where color of button changes with selected color

        :param mesh_color_button: Whether it controls mesh color or background color
        """
        super(ColorButton, self).__init__(*args, **kwargs)

        # Color
        self.color = None
        self.settings_widget = None
        self.setMaximumSize(30, 15)
        self.mesh_color_button = mesh_color_button

        # Click the
        self.clicked.connect(self.show_dialog)

    def connect_settings(self, settings_widget) -> None:
        """Connect the settings object so the button can change the settings

        :param settings_widget: Contains the pushbutton
        """
        self.settings_widget = settings_widget

        # Get the color and convert it to rgb
        if self.mesh_color_button:
            rgb_color = self.settings_widget.settings.mesh_color
        else:
            rgb_color = self.settings_widget.settings.background_color

        rgb_color = [component * 255 for component in rgb_color]

        # First set color so, it doesn't draw on the screen
        self.color = QColor(*rgb_color)
        self.set_color(self.color)

    def set_color(self, color: QColor) -> None:
        """Set the color of the pushbutton by changing the background

        :param color: Color to set the button to
        """
        # Color is not different, still set the border
        if color == self.color:
            self.setStyleSheet(f"background-color: #{self.hex()}; border: 1px solid")
            return

        self.color = color
        self.setStyleSheet(f"background-color: #{self.hex()}; border: 1px solid")

        if not self.settings_widget:
            logging.warning("Setting color whilst there is no connected component")
            return

        if self.mesh_color_button:
            self.settings_widget.settings.mesh_color = self.float_list()
        else:
            self.settings_widget.settings.background_color = self.float_list()

        self.settings_widget.apply_settings()

    def show_dialog(self) -> None:
        """Show color-picker dialog to select color.

        Qt will use the native dialog by default.
        """
        color: QColor = QColorDialog.getColor()
        if color.isValid():
            self.set_color(color)

    def float_list(self) -> (float, float, float):
        """Convert color to list of RGB values

        :return: List of RGB values
        """
        return self.color.redF(), self.color.greenF(), self.color.blueF()

    # Source: https://www.educative.io/answers/how-to-convert-hex-to-rgb-and-rgb-to-hex-in-python
    def hex(self) -> str:
        """Convert color to hex format

        :return: Hex format of color
        """
        return '{:02X}{:02X}{:02X}'.format(self.color.red(), self.color.green(), self.color.blue())

    def mousePressEvent(self, e) -> None:
        """Resets color to white on mouseclick

        :param e: Event
        """
        if e.button() == Qt.MouseButton.RightButton:
            self.set_color(QColor(255, 255, 255))

        return super(ColorButton, self).mousePressEvent(e)

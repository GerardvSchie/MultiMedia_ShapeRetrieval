import logging

from PyQt6.QtGui import QPalette, QColor
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QPushButton, QColorDialog, QStyle


# Source: https://www.pythonguis.com/widgets/qcolorbutton-a-color-selector-tool-for-pyqt/
# Source: https://zetcode.com/pyqt6/dialogs/
class ColorButton(QPushButton):
    """
    Custom Qt Widget to show a chosen color.

    Left-clicking the button shows the color-chooser, while
    right-clicking resets the color to None (no-color).
    """
    def __init__(self, *args, **kwargs):
        super(ColorButton, self).__init__(*args, **kwargs)

        self.color = None
        self.settings_widget = None
        self.setMaximumHeight(15)

        self.clicked.connect(self.show_dialog)

    def connect_settings(self, settings_widget):
        self.settings_widget = settings_widget

        # Get the color and convert it to rgb
        mesh_color = self.settings_widget.settings.mesh_color
        mesh_color = [component * 255 for component in mesh_color]

        # First set color so, it doesn't draw on the screen
        self.color = QColor(mesh_color[0], mesh_color[1], mesh_color[2])
        self.set_color(self.color)

    def set_color(self, color: QColor):
        # Color is not different, still set the border
        if color == self.color:
            self.setStyleSheet(f"background-color: #{self.hex()}; border: 1px solid")
            return

        self.color = color
        self.setStyleSheet(f"background-color: #{self.hex()}; border: 1px solid")

        if not self.settings_widget:
            logging.warning("Setting color whilst there is no connected component")
            return

        self.settings_widget.settings.mesh_color = self.float_list()
        self.settings_widget.apply_settings()

    def show_dialog(self):
        """
        Show color-picker dialog to select color.

        Qt will use the native dialog by default.
        """
        color: QColor = QColorDialog.getColor()
        if color.isValid():
            self.set_color(color)

    def float_list(self) -> [float]:
        return self.color.redF(), self.color.greenF(), self.color.blueF()

    def hex(self) -> str:
        return '{:02X}{:02X}{:02X}'.format(self.color.red(), self.color.green(), self.color.blue())

    def mousePressEvent(self, e):
        if e.button() == Qt.MouseButton.RightButton:
            self.set_color(QColor(1, 1, 1))

        return super(ColorButton, self).mousePressEvent(e)

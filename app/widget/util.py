from PyQt6.QtWidgets import QWidget, QLabel
from PyQt6.QtGui import QPalette, QColor
from PyQt6.QtCore import Qt

from app.util.font import BOLD_FONT


def color_widget(widget: QWidget, rgb: [int]) -> None:
    """Color a widget in the GUI, currently does an early exit since this is only for debug

    :param widget: Widget to color
    :param rgb: Color to give the widget object
    """
    return

    widget.setAutoFillBackground(True)
    widget.setPalette(QPalette(QColor(rgb[0], rgb[1], rgb[2])))


def create_header_label(text: str) -> QLabel:
    """Creates a header containing the text in a bold label

    :param text: Text to put in the header
    :return: Label containing the text in bold and large font size
    """
    header_label = QLabel(text)
    header_label.setFont(BOLD_FONT)
    header_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    header_label.setMaximumHeight(20)
    return header_label

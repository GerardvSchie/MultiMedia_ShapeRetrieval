from PyQt6.QtWidgets import QWidget, QLabel
from PyQt6.QtGui import QPalette, QColor
from PyQt6.QtCore import Qt

from app.util.font import BOLD_FONT


def color_widget(widget: QWidget, rgb: [int]) -> None:
    return

    widget.setAutoFillBackground(True)
    widget.setPalette(QPalette(QColor(rgb[0], rgb[1], rgb[2])))


def create_header_label(text: str) -> QLabel:
    header_label = QLabel(text)
    header_label.setFont(BOLD_FONT)
    header_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    header_label.setMaximumHeight(20)
    return header_label

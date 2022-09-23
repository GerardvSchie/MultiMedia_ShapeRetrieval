from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QPalette, QColor


def color_widget(widget: QWidget, rgb: [int]):
    widget.setAutoFillBackground(True)
    widget.setPalette(QPalette(QColor(rgb[0], rgb[1], rgb[2])))

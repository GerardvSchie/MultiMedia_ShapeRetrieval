from app.util.font import BOLD_FONT, ITALIC_FONT

from PyQt6.QtWidgets import QGridLayout, QWidget, QLabel
from PyQt6.QtCore import Qt


class GridLayout(QGridLayout):
    def __init__(self):
        super(GridLayout, self).__init__()

        self.setAlignment(Qt.AlignmentFlag.AlignTop)
        self._current_row_index = 0

    def add_header(self, header_title: str):
        header_label = QLabel(header_title)
        header_label.setFont(BOLD_FONT)
        header_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.addWidget(header_label, self._current_row_index, 0, 1, -1)
        self._current_row_index += 1

    def add_section(self, section_title: str):
        section_label = QLabel(section_title)
        section_label.setFont(BOLD_FONT)

        self.addWidget(section_label, self._current_row_index, 0, 1, -1)
        self._current_row_index += 1

    def add_row(self, label_text: str, widget: QWidget):
        row_label = QLabel(label_text)
        row_label.setFont(ITALIC_FONT)

        self.addWidget(row_label, self._current_row_index, 0)
        self.addWidget(widget, self._current_row_index, 1)
        self._current_row_index += 1

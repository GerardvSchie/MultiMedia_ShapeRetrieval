from app.util.font import BOLD_FONT, ITALIC_FONT

from PyQt6.QtWidgets import QGridLayout, QWidget, QLabel
from PyQt6.QtCore import Qt


class GridLayout(QGridLayout):
    def __init__(self):
        """Create gridlayout and align to the middle"""
        super(GridLayout, self).__init__()

        self.setAlignment(Qt.AlignmentFlag.AlignTop)
        self._current_row_index = 0

    def add_header(self, header_title: str) -> None:
        """Add a centered bold header to the top

        :param header_title: Title of the header
        """
        header_label = QLabel(header_title)
        header_label.setFont(BOLD_FONT)
        header_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Add label to the grid
        self.addWidget(header_label, self._current_row_index, 0, 1, -1)
        self._current_row_index += 1

    def add_section(self, section_title: str) -> None:
        """Section header in bold

        :param section_title: Title of the label
        """
        section_label = QLabel(section_title)
        section_label.setFont(BOLD_FONT)

        self.addWidget(section_label, self._current_row_index, 0, 1, -1)
        self._current_row_index += 1

    def add_row(self, label_text: str, widgets: [QWidget]):
        """Adds a row, starting with some text and then a list of widgets

        :param label_text: Text of the label at index 0
        :param widgets: Widgets to add in a row
        """
        # Add label
        row_label = QLabel(label_text)
        row_label.setFont(ITALIC_FONT)
        self.addWidget(row_label, self._current_row_index, 0)

        # Add all widgets afterwards, make sure the final one spans the entire length of the row
        for widget_index in range(len(widgets)):
            if widget_index == len(widgets) - 1:
                self.addWidget(widgets[widget_index], self._current_row_index, widget_index + 1, 1, -1)
            else:
                self.addWidget(widgets[widget_index], self._current_row_index, widget_index + 1, 1, 1)

        self._current_row_index += 1

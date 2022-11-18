from PyQt6.QtWidgets import QTableWidget, QTableWidgetItem
from PyQt6.QtCore import Qt
import numpy as np
import os

from src.object.shape import Shape


class TableWidget(QTableWidget):
    def __init__(self, shape_list: [Shape], get_row, headers: list[str]):
        """Create the table widget by setting the header and all the values

        :param shape_list: List of shapes which values need to be put in the table
        :param get_row: Function to get the row values in the database
        :param headers: List of headers
        """
        super(TableWidget, self).__init__()

        # Set columns and rows in QTableWidget
        self.setColumnCount(len(headers))
        self.setRowCount(len(shape_list))
        self.setSortingEnabled(True)

        # Fill database header and the table
        self.fill_header(headers)
        self.fill_table(shape_list, get_row)

    def fill_header(self, headers: list[str]) -> None:
        """Create the header in the table

        :param headers: List of names of the headers
        """
        for column_index in range(len(headers)):
            item: QTableWidgetItem = QTableWidgetItem(headers[column_index].replace('_', ' '))
            item.setFlags(Qt.ItemFlag.ItemIsEnabled)
            self.setHorizontalHeaderItem(column_index, item)

    def fill_table(self, shape_list: [Shape], get_row) -> None:
        """Fill table with values of the shape list

        :param shape_list: List of shape to fill the table with
        :param get_row: Function to get the values in
        """
        row_nr = 0
        # Loops to add values into QTableWidget
        # Lock items: https://stackoverflow.com/questions/7727863/how-to-make-a-cell-in-a-qtablewidget-read-only
        for shape in shape_list:
            column_nr = 0

            # Value in the shape
            for row_value in get_row(shape):
                do_str = type(row_value) is np.ndarray or (type(row_value) is float and np.isinf(row_value))

                # Create path from the array
                if column_nr == 0:
                    row_value = os.path.join(*row_value)

                # To properly sort the numerical values they need to be numbers
                # Source numerical: https://stackoverflow.com/questions/60512920/sorting-numbers-in-qtablewidget-work-doesnt-right-pyqt5
                item: QTableWidgetItem = QTableWidgetItem()
                if do_str:
                    item.setData(0, str(row_value))
                else:
                    item.setData(0, row_value)

                # Set the item
                item.setFlags(Qt.ItemFlag.ItemIsEnabled)
                self.setItem(row_nr, column_nr, item)
                column_nr += 1

            # Next row
            row_nr += 1

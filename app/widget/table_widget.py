from PyQt6.QtWidgets import QTableWidget, QTableWidgetItem
from PyQt6.QtCore import Qt
import numpy as np
import os


class TableWidget(QTableWidget):
    def __init__(self, shape_list, get_row, headers: list[str]):
        super(TableWidget, self).__init__()

        # Set columns and rows in QTableWidget
        self.setColumnCount(len(headers))
        self.setRowCount(len(shape_list))
        self.setSortingEnabled(True)

        self.fill_header(headers)
        self.fill_table(shape_list, get_row)

    def fill_header(self, headers: list[str]):
        for column_index in range(len(headers)):
            item: QTableWidgetItem = QTableWidgetItem(headers[column_index].replace('_', ' '))
            item.setFlags(Qt.ItemFlag.ItemIsEnabled)
            self.setHorizontalHeaderItem(column_index, item)

    def fill_table(self, shape_list, get_row):
        row_nr = 0
        # Loops to add values into QTableWidget
        # Lock items: https://stackoverflow.com/questions/7727863/how-to-make-a-cell-in-a-qtablewidget-read-only
        for shape in shape_list:
            column_nr = 0
            for row_value in get_row(shape):
                do_str = type(row_value) is np.ndarray or (type(row_value) is float and np.isinf(row_value))

                if column_nr == 0:
                    row_value = os.path.join(*row_value)

                # Source numerical https://stackoverflow.com/questions/60512920/sorting-numbers-in-qtablewidget-work-doesnt-right-pyqt5
                item: QTableWidgetItem = QTableWidgetItem()
                if do_str:
                    item.setData(0, str(row_value))
                else:
                    item.setData(0, row_value)

                item.setFlags(Qt.ItemFlag.ItemIsEnabled)
                self.setItem(row_nr, column_nr, item)
                column_nr += 1
            row_nr += 1

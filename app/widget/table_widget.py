from PyQt6.QtWidgets import QTableWidget, QTableWidgetItem
from PyQt6.QtCore import Qt

from src.database.reader import DatabaseReader
from src.object.descriptors import Descriptors

COLUMNS = ['surface_area', 'compactness', 'rectangularity', 'diameter', 'eccentricity']


class TableWidget(QTableWidget):
    def __init__(self):
        super(TableWidget, self).__init__()

        descriptors: dict[str, Descriptors] = DatabaseReader.read_descriptors('data/database/original_descriptors.csv')

        # Set columns and rows in QTableWidget
        self.setColumnCount(len(COLUMNS) + 1)
        self.setRowCount(len(descriptors))
        self.setSortingEnabled(True)

        self.fill_header()
        self.fill_table(descriptors)

    def fill_header(self):
        for column_index in range(len(COLUMNS)):
            item: QTableWidgetItem = QTableWidgetItem(COLUMNS[column_index])
            item.setFlags(Qt.ItemFlag.ItemIsEnabled)
            self.setHorizontalHeaderItem(column_index + 1, item)

    def fill_table(self, descriptors):
        row_nr = 0
        # Loops to add values into QTableWidget
        # Lock items: https://stackoverflow.com/questions/7727863/how-to-make-a-cell-in-a-qtablewidget-read-only
        for identifier in descriptors:
            item: QTableWidgetItem = QTableWidgetItem(identifier)
            item.setFlags(Qt.ItemFlag.ItemIsEnabled)
            self.setItem(row_nr, 0, item)

            column_nr = 1

            for column in COLUMNS:
                item: QTableWidgetItem = QTableWidgetItem(str(descriptors[identifier].__getattribute__(column)))
                item.setFlags(Qt.ItemFlag.ItemIsEnabled)
                self.setItem(row_nr, column_nr, item)
                column_nr += 1
            row_nr += 1

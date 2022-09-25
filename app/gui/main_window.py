from PyQt6.QtWidgets import QMainWindow
from PyQt6.QtGui import QFont

from app.widget.tab_widget import TabWidget
from app.gui.menu_bar import MenuBar
from app.util.font import FONT


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setFont(QFont(FONT))

        # Add menu bar
        self.menu_bar: MenuBar = MenuBar(self.menuBar())

        # Add tabs
        self.tab_widget: TabWidget = TabWidget()
        self.setCentralWidget(self.tab_widget)

    # Need to close the open3d handlers separately
    def closeEvent(self, *args, **kwargs):
        self.tab_widget.closeEvent(*args, **kwargs)

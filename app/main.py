import sys
import src.util.logger as logger
from app.gui.main_window import MainWindow

from PyQt6 import QtWidgets


def main():
    app = QtWidgets.QApplication(sys.argv)
    form = MainWindow()
    form.setWindowTitle('o3d Embed')
    form.setGeometry(100, 100, 600, 500)
    form.show()
    sys.exit(app.exec())


# Example loads an .off and .ply file
if __name__ == '__main__':
    logger.initialize()
    main()

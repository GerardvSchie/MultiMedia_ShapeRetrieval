import sys
import glfw

import os

# Needed to fix ModuleNotFoundError when importing src.util.logger.
directoryContainingCurrentFile = os.path.dirname(__file__)
repoDirectory = os.path.dirname(directoryContainingCurrentFile)

# Add repo to list of possible paths
import sys
sys.path.append(repoDirectory)

import src.util.logger as logger
from src.util.io import check_working_dir
from app.gui.main_window import MainWindow

from PyQt6 import QtWidgets


def main():
    app = QtWidgets.QApplication(sys.argv)
    form = MainWindow()
    form.setWindowTitle('o3d Embed')
    form.setGeometry(100, 100, 600, 500)
    form.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    logger.initialize()
    check_working_dir()
    main()

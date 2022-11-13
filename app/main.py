# Add repo to list of possible paths
import sys
import os
from PyQt6 import QtWidgets
import matplotlib

# Needed to fix ModuleNotFoundError when importing src.util.logger.
directoryContainingCurrentFile = os.path.dirname(__file__)
repoDirectory = os.path.dirname(directoryContainingCurrentFile)

sys.path.append(repoDirectory)

import src.util.logger as logger
from src.util.io import check_working_dir
from app.gui.main_window import MainWindow


def main():
    app = QtWidgets.QApplication(sys.argv)
    form = MainWindow()
    form.setWindowTitle('Multimedia Retrieval')
    form.setGeometry(100, 100, 1000, 700)
    app.focusWindow()
    form.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    logger.initialize()
    matplotlib.use('Qt5Agg')
    check_working_dir()
    main()

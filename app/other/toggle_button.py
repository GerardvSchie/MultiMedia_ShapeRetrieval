from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QPushButton


# Source: https://www.geeksforgeeks.org/pyqt5-toggle-button/
class ToggleButton(QPushButton):
    def __init__(self, icon_path: str, *args, **kwargs):
        """Toggle button, like enable wireframe view or disabling it

        :param icon_path: Path of
        """
        super(ToggleButton, self).__init__(*args, **kwargs)

        self.setMaximumSize(15, 15)
        self.setCheckable(True)
        self.clicked.connect(self.toggle_button)
        self.setStyleSheet("background-color : lightgrey")

        self.setIcon(QIcon(icon_path))

    def toggle_button(self) -> None:
        """Toggle color of button based on state"""
        # if button is checked
        if self.isChecked():
            # setting background color to light-blue
            self.setStyleSheet("background-color : lightblue")
        # if it is unchecked
        else:
            # set background color back to light-grey
            self.setStyleSheet("background-color : lightgrey")

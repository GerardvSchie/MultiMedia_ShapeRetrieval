from PyQt6.QtGui import QWindow

from src.object.settings import Settings
from app.widget.visualization_widget import VisualizationWidget


class VisualizationWindow(QWindow):
    def __init__(self, settings: Settings):
        """Creates visualization window with the scene

        :param settings: Settings for the widget, like should it show the convex hull
        """
        super(VisualizationWindow, self).__init__()

        # Settings
        self.visualization_widget = VisualizationWidget(settings)

        self.current_window_type = -1
        self.fromWinId(self.visualization_widget.hwnd)

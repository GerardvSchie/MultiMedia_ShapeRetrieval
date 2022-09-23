from PyQt6.QtGui import QWindow
from src.object.settings import Settings
from app.widget.visualization_widget import VisualizationWidget


class VisualizationWindow(QWindow):
    def __init__(self, settings: Settings):
        super(VisualizationWindow, self).__init__()

        # Settings
        self.visualization_widget = VisualizationWidget(settings)

        self.current_window_type = -1
        self.fromWinId(self.visualization_widget.hwnd)

        #
        #
        # # Visible=False so it does not open separate window
        # window = QtGui.QWindow.fromWinId(self.visualization_widget.hwnd)
        # window_container = self.create(window, scene_widget)

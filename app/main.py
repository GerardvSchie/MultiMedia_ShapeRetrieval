import open3d.visualization.gui as gui
import sys
import os
import open3d.visualization as visualization

import open3d as o3d
import win32gui
import sys
import threading
import time

from app.gui.app_window import AppWindow
import src.util.logger as logger


def main():
    # We need to initalize the application, which finds the necessary shaders
    # for rendering and prepares the cross-platform window abstraction.
    gui.Application.instance.initialize()

    w = AppWindow(1024, 768)

    if len(sys.argv) > 1:
        path = sys.argv[1]
        if os.path.exists(path):
            w.scene_widget.load(path)
        else:
            w.window.show_message_box("Error",
                                      "Could not open file '" + path + "'")

    # Run the event loop. This will not return until the last window is closed.
    gui.Application.instance.run()


# Example loads an .off and .ply file
if __name__ == '__main__':
    logger.initialize()
    main()

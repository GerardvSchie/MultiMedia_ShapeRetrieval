import polygon_loader
import open3d as o3d
import open3d.visualization.gui as gui
import sys
import os

from gui.AppWindow import AppWindow


def main():
    # We need to initalize the application, which finds the necessary shaders
    # for rendering and prepares the cross-platform window abstraction.
    gui.Application.instance.initialize()

    w = AppWindow(1024, 768)

    if len(sys.argv) > 1:
        path = sys.argv[1]
        if os.path.exists(path):
            w.load(path)
        else:
            w.window.show_message_box("Error",
                                      "Could not open file '" + path + "'")

    # Run the event loop. This will not return until the last window is closed.
    gui.Application.instance.run()


# Example loads an .off and .ply file
if __name__ == '__main__':
    off_example = polygon_loader.load_file("example.off")
    print(off_example)
    ply_example = polygon_loader.load_file("example.ply")
    print(ply_example)

    # Visualize both objects
    o3d.visualization.draw_geometries([off_example, ply_example])
    main()

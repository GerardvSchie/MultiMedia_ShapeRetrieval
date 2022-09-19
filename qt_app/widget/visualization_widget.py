import logging
import open3d as o3d
import win32gui


from PyQt6 import QtWidgets, QtGui, QtCore


class VisualizationWidget(QtWidgets.QWidget):
    def __init__(self, showWireFrame):
        super(VisualizationWidget, self).__init__()
        self.shape = None

        file_path = "C:\\Users\\gerard\\MegaDrive\\Documents\\M2.1-MultiMedia_Retrieval\\Assignment\\data\\example.off"
        self.pcd = o3d.io.read_triangle_mesh(file_path)

        self.widget = QtWidgets.QWidget()
        self.vis = o3d.visualization.VisualizerWithEditing()
        # Visible=False so it does not open separate window
        self.vis.create_window(visible=False)
        self.hwnd = win32gui.FindWindowEx(0, 0, None, "Open3D - free view")

        if showWireFrame:
            render_option: o3d.visualization.RenderOption = self.vis.get_render_option()
            render_option.mesh_show_wireframe = True

        self.vis.add_geometry(self.pcd)

        # self.thread = QtCore.QThread()
        # self.worker = Worker()
        # self.thread.started.connect(lambda: self.worker.run([self.vis]))
        # self.thread.start()

    def initialize(self):
        pass

    # # Part of the scene, what is in the window
    # def load_shape(self, path):
    #     # Here the widget is initialized
    #     self.vis.clear_geometry()
    #     self.shape = Shape(path, load_shape=True)
    #     FeatureExtractor.extract_features(self.shape)
    #
    #     if self.shape.geometry is not None:
    #         try:
    #             self.vis.scene.add_geometry("__model__", self.shape.geometry,
    #                                            self.settings_widget.settings.material)
    #
    #             bounds = self.shape.geometry.get_axis_aligned_bounding_box()
    #             self.widget.setup_camera(60, bounds, bounds.get_center())
    #             self.property_widget.update_properties(self.shape.features)
    #         except Exception as e:
    #             logging.error(f"Loading of shape failed with message: {e}")

    def start_vis(self):
        self.vis.run()

    def update_vis(self):
        # self.vis.update_geometry(self.shape.geometry)
        self.vis.poll_events()
        self.vis.update_renderer()

import open3d.visualization.gui as gui


class Settings:
    def __init__(self):
        # Colors
        self.background_color: [float] = (1, 1, 1)
        self.mesh_color: [float] = (1, 1, 1)
        # self.point_cloud_color = gui.Color()
        # self.convex_hull_color: [float] = (1, 0, 0)
        # self.axis_aligned_bounding_box_color: [float] = (1, 0, 1)

        # Render settings
        self.show_mesh: bool = True
        self.show_point_cloud: bool = False
        self.show_convex_hull: bool = False
        self.show_axis_aligned_bounding_box: bool = False

        self.show_silhouette: bool = False
        self.show_wireframe: bool = False
        self.show_axes: bool = False

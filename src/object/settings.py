import open3d.visualization.gui as gui


class Settings:
    def __init__(self):
        # Colors
        self.background_color = gui.Color(1, 1, 1)
        self.mesh_color = gui.Color(1, 1, 1)
        # self.point_cloud_color = gui.Color()
        self.convex_hull_color = gui.Color(1, 0, 0)

        # Render settings
        self.light_on = True
        self.show_mesh = True
        self.show_wireframe = False
        self.show_point_cloud = False
        self.show_convex_hull = False
        self.show_axes = False

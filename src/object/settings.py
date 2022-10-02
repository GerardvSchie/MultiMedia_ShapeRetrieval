from __future__ import annotations


class Settings:
    def __init__(self):
        # Colors
        self.background_color: [float] = (1, 1, 1)
        self.mesh_color: [float] = (2/3, 2/3, 1)

        # Render settings
        self.show_mesh: bool = True
        self.show_point_cloud: bool = False
        self.show_convex_hull: bool = False
        self.show_axis_aligned_bounding_box: bool = False
        self.show_center_mesh: bool = False

        self.show_silhouette: bool = False
        self.show_wireframe: bool = False
        self.show_normals: bool = False
        self.show_axes: bool = False

    def update(self, settings: Settings):
        self.background_color = settings.background_color
        self.mesh_color = settings.mesh_color

        # Render settings
        self.show_mesh = settings.show_mesh
        self.show_point_cloud = settings.show_point_cloud
        self.show_convex_hull = settings.show_convex_hull
        self.show_axis_aligned_bounding_box = settings.show_axis_aligned_bounding_box
        self.show_center_mesh = settings.show_center_mesh

        # Additional options
        self.show_silhouette = settings.show_silhouette
        self.show_axes = settings.show_axes

    def clear_meshes(self):
        self.show_mesh = False
        self.show_point_cloud = False
        self.show_convex_hull = False
        self.show_axis_aligned_bounding_box = False
        self.show_axes = False
        self.show_center_mesh = False

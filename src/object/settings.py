from __future__ import annotations


class Settings:
    def __init__(self):
        """Initial state of the visualization settings"""
        # Colors
        self.background_color: [float] = (1.0, 1.0, 1.0)
        self.mesh_color: [float] = (2/3, 2/3, 1.0)
        self.point_size: int = 3

        # Render settings
        self.show_mesh: bool = True
        self.show_point_cloud: bool = False
        self.show_convex_hull: bool = False
        self.show_axis_aligned_bounding_box: bool = False
        self.show_center_mesh: bool = False

        # Visualization modes
        self.show_silhouette: bool = False
        self.show_wireframe: bool = False
        self.show_normals: bool = False
        self.show_axes: bool = False

    def update(self, settings: Settings) -> None:
        """Update the current settings with the given settings

        :param settings: New settings
        """
        # Generic settings
        self.background_color = settings.background_color
        self.mesh_color = settings.mesh_color
        self.point_size = settings.point_size

        # Render settings
        self.show_mesh = settings.show_mesh
        self.show_point_cloud = settings.show_point_cloud
        self.show_convex_hull = settings.show_convex_hull
        self.show_axis_aligned_bounding_box = settings.show_axis_aligned_bounding_box
        self.show_center_mesh = settings.show_center_mesh

        # Additional options
        self.show_silhouette = settings.show_silhouette
        self.show_axes = settings.show_axes

    def clear_meshes(self) -> None:
        """Resets the settings state to a clear state"""
        self.show_mesh = False
        self.show_point_cloud = False
        self.show_convex_hull = False
        self.show_axis_aligned_bounding_box = False
        self.show_axes = False
        self.show_center_mesh = False

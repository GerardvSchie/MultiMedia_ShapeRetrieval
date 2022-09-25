import os.path
import logging
import open3d as o3d
import numpy as np
import open3d.cpu.pybind.geometry


class Geometries:
    def __init__(self, path: str):
        self.path: str = path

        self.mesh: o3d.geometry.TriangleMesh = None
        self.point_cloud: o3d.geometry.PointCloud = None
        self.convex_hull_mesh: o3d.geometry.TriangleMesh = None
        self.convex_hull_line_set: o3d.geometry.LineSet = None
        self.axis_aligned_bounding_box_line_set: o3d.geometry.LineSet = None
        self.axes: o3d.geometry.TriangleMesh = None

    # A big portion of these two methods comes from the open3d example, see license in app folder.
    def load(self):
        self.load_mesh()
        self.load_point_cloud()
        self.load_convex_hull()
        self.load_coordinate_axes()
        self.load_axis_aligned_bounding_box()

    def load_mesh(self) -> bool:
        # Mesh is already loaded
        if self.mesh:
            return True

        geometry_type = o3d.io.read_file_geometry_type(self.path)

        if geometry_type & o3d.io.CONTAINS_TRIANGLES:
            self.mesh: open3d.cpu.pybind.geometry.TriangleMesh = o3d.io.read_triangle_mesh(self.path)
            self.mesh.orient_triangles()

        # Could not load mesh
        if self.mesh is None:
            logging.warning(
                f"Shape at path '{os.path.abspath(self.path)}' appears to be a point cloud, cannot load mesh")
            return False

        # No triangles in the mesh
        if len(self.mesh.triangles) == 0:
            logging.warning(f"Shape at path '{os.path.abspath(self.path)}' has 0 triangles, will read as point cloud")
            self.mesh = None
            return False

        # Get the normals of the mesh
        self.mesh.compute_vertex_normals()
        if len(self.mesh.vertex_colors) == 0:
            self.mesh.paint_uniform_color([1, 1, 1])

        # Make sure the mesh has texture coordinates
        if not self.mesh.has_triangle_uvs():
            uv = np.array([[0.0, 0.0]] * (3 * len(self.mesh.triangles)))
            self.mesh.triangle_uvs = o3d.utility.Vector2dVector(uv)

        return True

    def load_point_cloud(self) -> bool:
        # Point cloud already existed
        if self.point_cloud:
            return True

        try:
            self.point_cloud: o3d.geometry.PointCloud = o3d.io.read_point_cloud(self.path)
        except Exception as ex:
            logging.error(ex)
            return False

        if not self.point_cloud:
            logging.warning("Failed to read point cloud")
            return False

        return True

    def load_convex_hull(self) -> bool:
        if self.convex_hull_mesh:
            return True

        if not self.load_mesh():
            return False

        self.convex_hull_mesh, _ = self.mesh.compute_convex_hull()
        self.convex_hull_line_set = o3d.geometry.LineSet.create_from_triangle_mesh(self.convex_hull_mesh)
        self.convex_hull_line_set.paint_uniform_color((1, 0, 0))
        return True

    def load_axis_aligned_bounding_box(self) -> bool:
        if self.axis_aligned_bounding_box_line_set:
            return True

        if not self.load_mesh():
            return False

        axis_aligned_bounding_box = self.mesh.get_axis_aligned_bounding_box()
        self.axis_aligned_bounding_box_line_set = o3d.geometry.LineSet.create_from_axis_aligned_bounding_box(axis_aligned_bounding_box)
        self.axis_aligned_bounding_box_line_set.paint_uniform_color((1, 0, 1))
        return True

    def load_coordinate_axes(self) -> bool:
        if self.axes:
            return True

        if not self.load_mesh():
            logging.error("Cannot compute coordinate axes of ")
            return False

        self.axes = self.mesh.create_coordinate_frame(0.1)
        return True

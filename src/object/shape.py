import os.path
import logging
import open3d as o3d
import numpy as np
import open3d.cpu.pybind.geometry

from src.object.features import Features


class Shape:
    def __init__(self, shape_path, pre_computed_features=None, load_shape=False):
        if not os.path.exists(shape_path):
            logging.error(f"Shape file at path {os.path.abspath(shape_path)} does not exist!")

        # Convert shape file to .ply format, so we can extract point cloud
        self.path = os.path.relpath(shape_path)
        self.convert_to_ply()

        self.mesh = None
        self.point_cloud = None
        self.convex_hull = None

        if pre_computed_features:
            self.features = pre_computed_features
        else:
            # Separate path based on separator of os system
            self.features = Features()
            self.features.true_class = os.path.split(os.path.split(shape_path)[0])[1]

        if load_shape:
            self.load()

    # A big portion of these two methods comes from the open3d example, see license in app folder.
    def load(self):
        self.load_mesh()
        self.load_point_cloud()
        self.load_convex_hull()

    def convert_to_ply(self):
        new_file_path = self.path.split(".")[0] + ".ply"

        # Ply file already computed, set path to the ply file
        if os.path.exists(new_file_path):
            self.path = new_file_path
            return

        mesh = o3d.io.read_triangle_mesh(self.path)
        # mesh.orient_triangles()

        o3d.io.write_triangle_mesh(new_file_path, mesh)
        self.path = new_file_path

    def load_mesh(self):
        # Mesh is already loaded
        if self.mesh:
            return

        geometry_type = o3d.io.read_file_geometry_type(self.path)

        if geometry_type & o3d.io.CONTAINS_TRIANGLES:
            self.mesh: open3d.cpu.pybind.geometry.TriangleMesh = o3d.io.read_triangle_mesh(self.path)
            self.mesh.orient_triangles()

        # Could not load mesh
        if self.mesh is None:
            logging.warning(f"Shape at path '{os.path.abspath(self.path)}' appears to be a point cloud, cannot load mesh")
            return

        # No triangles in the mesh
        if len(self.mesh.triangles) == 0:
            logging.debug(f"Shape at path '{os.path.abspath(self.path)}' has 0 triangles, will read as point cloud")
            self.mesh = None
            return

        # Get the normals of the mesh
        self.mesh.compute_vertex_normals()
        if len(self.mesh.vertex_colors) == 0:
            self.mesh.paint_uniform_color([1, 1, 1])

        # Make sure the mesh has texture coordinates
        if not self.mesh.has_triangle_uvs():
            uv = np.array([[0.0, 0.0]] * (3 * len(self.mesh.triangles)))
            self.mesh.triangle_uvs = o3d.utility.Vector2dVector(uv)

    def load_point_cloud(self):
        # Point cloud already existed
        if self.point_cloud:
            return

        try:
            self.point_cloud: o3d.geometry.PointCloud = o3d.io.read_point_cloud(self.path)
        except Exception as ex:
            logging.error(ex)

        if self.point_cloud is None:
            logging.warning("Failed to read point cloud")

    def load_convex_hull(self):
        if self.convex_hull:
            return

        self.load_point_cloud()

        if not self.point_cloud:
            return

        self.convex_hull, _ = self.point_cloud.compute_convex_hull()

    # Saves the mesh to the given file path
    def save(self, path):
        if not self.mesh:
            logging.warning(f"User tried to save whilst there is no mesh")

        if os.path.exists(path):
            logging.error(f"File at path {path} already exists, will not save")
            return

        o3d.io.write_triangle_mesh(path, self.mesh)

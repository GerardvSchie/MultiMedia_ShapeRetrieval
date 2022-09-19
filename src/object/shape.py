import os.path
import logging
import open3d as o3d
import numpy as np
from src.object.features import Features


class Shape:
    def __init__(self, shape_path, pre_computed_features=None, load_shape=False):
        if not os.path.exists(shape_path):
            logging.error(f"Shape file at path {os.path.abspath(shape_path)} does not exist!")

        self.path = os.path.relpath(shape_path)
        self.mesh = None
        self.geometry = None

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
        self.load_geometry()

    def load_mesh(self):
        # Mesh is already loaded
        if self.mesh:
            return

        geometry_type = o3d.io.read_file_geometry_type(self.path)

        if geometry_type & o3d.io.CONTAINS_TRIANGLES:
            self.mesh = o3d.io.read_triangle_mesh(self.path)

        # Could not load mesh
        if self.mesh is None:
            logging.warning(f"Shape at path '{os.path.abspath(self.path)}' appears to be a point cloud, cannot load mesh")

        # No triangles in the mesh
        if len(self.mesh.triangles) == 0:
            logging.debug(f"Shape at path '{os.path.abspath(self.path)}' has 0 triangles, will read as point cloud")
            self.mesh = None
            return

        # Get the normals of the mesh
        self.mesh.compute_vertex_normals()
        if len(self.mesh.vertex_colors) == 0:
            self.mesh.paint_uniform_color([1, 1, 1])

        self.geometry = self.mesh

        # Make sure the mesh has texture coordinates
        if self.mesh is not None and not self.mesh.has_triangle_uvs():
            uv = np.array([[0.0, 0.0]] * (3 * len(self.mesh.triangles)))
            self.mesh.triangle_uvs = o3d.utility.Vector2dVector(uv)

    def load_geometry(self):
        # Geometry is already loaded
        if self.geometry:
            return

        cloud = None
        try:
            cloud = o3d.io.read_point_cloud(self.path)
        except Exception as ex:
            logging.error(ex)

        if cloud is None:
            logging.warning("Failed to read point cloud")

        if not cloud.has_normals():
            cloud.estimate_normals()
        cloud.normalize_normals()
        self.geometry = cloud

    # Saves the mesh to the given file path
    def save(self, path):
        if not self.mesh:
            logging.warning(f"User tried to save whilst there is no mesh")

        if os.path.exists(path):
            logging.error(f"File at path {path} already exists, will not save")
            return

        o3d.io.write_triangle_mesh(path, self.mesh)

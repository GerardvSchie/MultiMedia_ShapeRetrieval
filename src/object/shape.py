import os.path
import logging
import numpy as np
import open3d as o3d
from src.object.features import Features
from src.pipeline.feature_extractor import FeatureExtractor


class Shape:
    def __init__(self, shape_path):
        self.mesh = None
        self.geometry = None

        if shape_path is not None:
            self.load(shape_path)

        self.features = Features()

    # Loads the file from a path
    # A big portion of this method comes from the open3d example, see license
    def load(self, path):
        logging.info(f"Loading shape from path: {path}")
        geometry_type = o3d.io.read_file_geometry_type(path)

        if geometry_type & o3d.io.CONTAINS_TRIANGLES:
            self.mesh = o3d.io.read_triangle_mesh(path)
        if self.mesh is not None:
            if len(self.mesh.triangles) == 0:
                logging.debug("Contains 0 triangles, will read as point cloud")
                self.mesh = None
            else:
                logging.info("Shape mesh loaded")
                self.mesh.compute_vertex_normals()
                if len(self.mesh.vertex_colors) == 0:
                    self.mesh.paint_uniform_color([1, 1, 1])
                self.geometry = self.mesh
            # Make sure the mesh has texture coordinates
            if self.mesh is not None and not self.mesh.has_triangle_uvs():
                logging.debug("Computing uvs since they are not in the file")
                uv = np.array([[0.0, 0.0]] * (3 * len(self.mesh.triangles)))
                self.mesh.triangle_uvs = o3d.utility.Vector2dVector(uv)
        else:
            logging.info(f"Shape appears to be a point cloud")

        if self.geometry is None:
            cloud = None
            try:
                cloud = o3d.io.read_point_cloud(path)
            except Exception:
                pass
            if cloud is not None:
                logging.info("Shape cloud loaded")
                if not cloud.has_normals():
                    cloud.estimate_normals()
                cloud.normalize_normals()
                self.geometry = cloud
            else:
                logging.warning("Failed to read points")

    # Saves the mesh to the given file path
    def save(self, path):
        if os.path.exists(path):
            logging.error(f"File at path {path} already exists, will not save")
            return

        o3d.io.write_triangle_mesh(path, self.mesh)

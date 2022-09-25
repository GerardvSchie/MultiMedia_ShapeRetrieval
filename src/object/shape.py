import os.path
import logging
import open3d as o3d

from src.object.features import Features
from src.object.geometries import Geometries


class Shape:
    def __init__(self, shape_path: str, pre_computed_features: Features = None, load_geometries: bool = False):
        if not os.path.exists(shape_path):
            logging.error(f"Shape file at path {os.path.abspath(shape_path)} does not exist!")
            raise Exception("Path does not exist")

        # Convert shape file to .ply format, so we can extract point cloud
        path = self.convert_to_ply(os.path.relpath(shape_path))

        if pre_computed_features:
            self.features: Features = pre_computed_features
        else:
            # Separate path based on separator of os system
            self.features: Features = Features()
            self.features.true_class = os.path.split(os.path.split(shape_path)[0])[1]

        self.geometries: Geometries = Geometries(path)
        if load_geometries:
            self.geometries.load()

    @staticmethod
    def convert_to_ply(path) -> str:
        new_file_path = path.split(".")[0] + ".ply"

        # Ply file already computed, set path to the ply file
        if os.path.exists(new_file_path):
            return new_file_path

        mesh = o3d.io.read_triangle_mesh(path)
        # mesh.orient_triangles()
        o3d.io.write_triangle_mesh(new_file_path, mesh)
        return new_file_path

    # Saves the mesh to the given file path
    def save(self, path):
        if not self.geometries.mesh:
            logging.error(f"User tried to save whilst there is no mesh")
            return

        if os.path.exists(path):
            logging.error(f"File at path {path} already exists, will not save")
            return

        o3d.io.write_triangle_mesh(path, self.geometries.mesh)

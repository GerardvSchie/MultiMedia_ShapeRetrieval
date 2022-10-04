import os.path
import logging
import open3d as o3d

from src.controller.geometries_controller import GeometriesController
from src.object.features.shape_features import ShapeFeatures
from src.object.geometries import Geometries


class Shape:
    def __init__(self, shape_path: str, pre_computed_features: ShapeFeatures = None, load_geometries: bool = False):
        if not os.path.exists(shape_path):
            logging.error(f"Shape file at path {os.path.abspath(shape_path)} does not exist!")
            raise Exception("Path does not exist")

        if pre_computed_features:
            self.features: ShapeFeatures = pre_computed_features
        else:
            self.features: ShapeFeatures = ShapeFeatures()

        # Convert shape file to .ply format, so we can extract point cloud
        path = self.convert_to_ply(os.path.relpath(shape_path))
        self.geometries: Geometries = Geometries(path)
        if load_geometries:
            GeometriesController.load_all_from_file(self.geometries)

    @staticmethod
    def convert_to_ply(path) -> str:
        dir_path, file_name = os.path.split(path)

        # If the name of the file is one of these, then we assume its created by the program
        if file_name == 'original.ply' or file_name == 'normalized.ply':
            return path

        shape_name, extension = file_name.split('.')
        new_file_path = os.path.join(dir_path, shape_name, 'original.ply')

        # Ply file already computed, set path to the ply file
        if os.path.exists(new_file_path):
            return new_file_path

        # Make path
        new_dir_path = os.path.join(dir_path, shape_name)
        os.makedirs(new_dir_path, exist_ok=True)

        # Read and save to .ply format under the new name
        mesh = o3d.io.read_triangle_mesh(path)
        o3d.io.write_triangle_mesh(new_file_path, mesh)
        return new_file_path

    # Saves the mesh to the given file path
    def save(self, path, force_save=False):
        if not self.geometries.mesh:
            logging.error(f"User tried to save whilst there is no mesh")
            return

        if os.path.exists(path) and not force_save:
            logging.error(f"File at path {path} already exists, will not save")
            return

        o3d.io.write_triangle_mesh(path, self.geometries.mesh)

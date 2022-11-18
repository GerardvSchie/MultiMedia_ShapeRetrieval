import os.path
import logging
import open3d as o3d

from src.controller.geometries_controller import GeometriesController
from src.object.descriptors import Descriptors
from src.object.features.shape_features import ShapeFeatures
from src.object.geometries import Geometries
from src.object.properties import Properties
from src.util.configs import *


class Shape:
    """Shape object contains information about the plots

    :param self.features: The single-value features of the shape
    :param self.descriptors: Descriptors, composed of applying a formula on te features
    :param self.geometries: Class containing the 3D objects of the shape
    :param self.properties: Properties of the shape, which are histograms saved in vectors
    """
    def __init__(self, shape_path: str, load_geometries: bool = False) -> None:
        """Create a shape

        :param shape_path: Path of the shape object
        :param load_geometries: Whether the 3D geometries need to get loaded in
        """
        if not os.path.exists(shape_path):
            logging.error(f"Shape file at path {os.path.abspath(shape_path)} does not exist!")
            raise Exception("Path does not exist")

        # Convert shape file to .ply format, so we can extract point cloud
        path = self.convert_to_ply(os.path.relpath(shape_path))

        self.features: ShapeFeatures = None
        self.descriptors: Descriptors = None
        self.geometries: Geometries = None
        self.properties: Properties = None

        self.set_new_ply_path(path)
        if load_geometries:
            GeometriesController.load_all_from_file(self.geometries)

    def set_new_ply_path(self, new_path: str) -> None:
        """Sets new path, and it resets all the features, descriptors, geometries, and propeties

        :param new_path: New path to replace it with
        """
        if not os.path.exists(new_path):
            logging.error(f"Shape file at path {os.path.abspath(new_path)} does not exist!")
            raise Exception("Path does not exist")

        if not new_path.endswith('.ply'):
            logging.error(f'Cannot set ply path to {new_path}')

        self.features: ShapeFeatures = ShapeFeatures()
        self.descriptors: Descriptors = Descriptors()
        self.geometries: Geometries = Geometries(new_path)
        self.properties: Properties = Properties()

    @staticmethod
    def convert_to_ply(path: str) -> str:
        """Converts *.off file to a *.ply file

        :param path: Existing path
        :return: New path to the ply file
        """
        dir_path, file_name = os.path.split(path)

        # If the name of the file is one of these, then we assume its created by the program itself
        if file_name == FILENAME_ORIGINAL or file_name == FILENAME_NORMALIZED_PCD or file_name == FILENAME_NORMALIZED_PLY:
            return path

        shape_name, extension = file_name.split('.')
        new_file_path = os.path.join(dir_path, shape_name, FILENAME_ORIGINAL)

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
    def save_ply(self, path: str) -> None:
        """Write mesh to a *.ply file

        :param path: Path to save it to
        """
        if not self.geometries.mesh:
            logging.error(f"User tried to save whilst there is no mesh")
            return

        # Name wrong if it isn't ending with ply
        if not path.endswith('.ply'):
            logging.warning(f'Wrong extension, use ".ply" instead of {path.split(".")[-1]}')
            return

        # Log if it will be overwritten
        if os.path.exists(path):
            logging.debug(f"File at path {path} already existed")

        # Write to file
        o3d.io.write_triangle_mesh(path, self.geometries.mesh)

    def save_pcd(self, path: str) -> None:
        """Saves point cloud in pcd file

        :param path: Path of the output ful
        """
        if not self.geometries.point_cloud:
            logging.error(f"User tried to save point cloud whilst it doesnt exist")
            return

        # Point cloud 
        if not path.endswith('.pcd'):
            logging.warning(f'Wrong extension, use ".pcd" instead of {path.split(".")[-1]}')
            return

        # Warn when file will be overriden
        if os.path.exists(path):
            logging.debug(f"File at path {path} already existed")

        # Writes point cloud to file
        o3d.io.write_point_cloud(path, self.geometries.point_cloud)

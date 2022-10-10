import csv
import os.path
import numpy as np

from src.object.features.bounding_box_features import BoundingBoxFeatures
from src.object.features.mesh_features import MeshFeatures
from src.object.features.shape_features import ShapeFeatures
from src.object.features.normalization_features import NormalizationFeatures

dataPaths = list()


class DatabaseReader:
    @staticmethod
    def read_all_shape_features() -> dict[str, ShapeFeatures]:
        shape_features = dict()

        os.makedirs('data/database/original', exist_ok=True)
        DatabaseReader.read_mesh_features(shape_features, 'data/database/original')
        DatabaseReader.read_convex_hull_features(shape_features, 'data/database/original')
        DatabaseReader.read_other_features(shape_features, 'data/database/original')
        DatabaseReader.read_normalization_features(shape_features, 'data/database/original')
        DatabaseReader.read_bounding_box_features(shape_features, 'data/database/original')

        return shape_features

    @staticmethod
    def read_mesh_features(shape_features: dict[str, ShapeFeatures], database_dir):
        database_path = os.path.join(database_dir, "mesh.csv")

        # Features file does not exist
        if not os.path.exists(database_path):
            return

        # File exists, load all features
        with open(database_path, "r") as f:
            reader = csv.reader(f)

            # Skip header
            next(reader)

            # Read the lines from the file
            for features in reader:
                data: MeshFeatures = MeshFeatures()

                identifier, data.nr_vertices, data.nr_faces, data.surface_area, data.volume, data.diameter \
                    = features

                # Reconstruct environment specific path, used numpy representation to be OS-invariant
                path = os.path.join(*(_read_np_array(identifier)))

                # Cast to types
                data.nr_vertices = int(data.nr_vertices)
                data.nr_faces = int(data.nr_faces)
                data.surface_area = float(data.surface_area)
                data.volume = float(data.volume)
                data.diameter = float(data.diameter)

                # Add to dict
                _add_if_not_exists(shape_features, path)
                shape_features[path].mesh_features = data

    @staticmethod
    def read_convex_hull_features(shape_features: dict[str, ShapeFeatures], database_dir):
        database_path = os.path.join(database_dir, "convex_hull.csv")

        # Features file does not exist
        if not os.path.exists(database_path):
            return

        # File exists, load all features
        with open(database_path, "r") as f:
            reader = csv.reader(f)

            # Skip header
            next(reader)

            # Read the lines from the file
            for features in reader:
                data: MeshFeatures = MeshFeatures()

                identifier, data.nr_vertices, data.nr_faces, data.surface_area, data.volume, data.diameter, \
                    = features

                # Reconstruct environment specific path, used numpy representation to be OS-invariant
                path = os.path.join(*(_read_np_array(identifier)))

                # Cast to types
                data.nr_vertices = int(data.nr_vertices)
                data.nr_faces = int(data.nr_faces)
                data.surface_area = float(data.surface_area)
                data.volume = float(data.volume)
                data.diameter = float(data.diameter)

                # Add to dict
                _add_if_not_exists(shape_features, path)
                shape_features[path].convex_hull_features = data

    @staticmethod
    def read_other_features(shape_features: dict[str, ShapeFeatures], database_dir):
        database_path = os.path.join(database_dir, "other.csv")

        # Features file does not exist
        if not os.path.exists(database_path):
            return

        # File exists, load all features
        with open(database_path, "r") as f:
            reader = csv.reader(f)

            # Skip header
            next(reader)

            # Read the lines from the file
            for features in reader:
                data: ShapeFeatures = ShapeFeatures()

                identifier, data.true_class = features

                # Reconstruct environment specific path, used numpy representation to be OS-invariant
                path = os.path.join(*(_read_np_array(identifier)))
                _add_if_not_exists(shape_features, path)

                # Assign to features
                shape_features[path].true_class = data.true_class

    @staticmethod
    def read_normalization_features(shape_features: dict[str, ShapeFeatures], database_dir):
        database_path = os.path.join(database_dir, "normalization.csv")

        # Features file does not exist
        if not os.path.exists(database_path):
            return

        # File exists, load all features
        with open(database_path, "r") as f:
            reader = csv.reader(f)

            # Skip header
            next(reader)

            # Read the lines from the file
            for features in reader:
                data: NormalizationFeatures = NormalizationFeatures()

                identifier, data.distance_to_center, data.scale, data.alignment, data.flip = features

                # Reconstruct environment specific path, used numpy representation to be OS-invariant
                path = os.path.join(*(_read_np_array(identifier)))
                _add_if_not_exists(shape_features, path)

                # Cast to types
                data.distance_to_center = float(data.distance_to_center)
                data.scale = float(data.scale)
                data.alignment = float(data.alignment)
                data.flip = float(data.flip)

                shape_features[path].normalization_features = data

    @staticmethod
    def read_bounding_box_features(shape_features: dict[str, ShapeFeatures], database_dir):
        database_path = os.path.join(database_dir, "bounding_box.csv")

        # Features file does not exist
        if not os.path.exists(database_path):
            return

        # File exists, load all features
        with open(database_path, "r") as f:
            reader = csv.reader(f)

            # Skip header
            next(reader)

            # Read the lines from the file
            for features in reader:
                data: BoundingBoxFeatures = BoundingBoxFeatures()

                identifier, data.min_bound, data.max_bound, data.surface_area, data.volume, data.diameter = features

                # Reconstruct environment specific path, used numpy representation to be OS-invariant
                path = os.path.join(*(_read_np_array(identifier)))
                _add_if_not_exists(shape_features, path)

                data.min_bound = _read_np_array(data.min_bound)
                data.max_bound = _read_np_array(data.max_bound)
                data.surface_area = float(data.surface_area)
                data.volume = float(data.volume)
                data.diameter = float(data.diameter)

                shape_features[path].axis_aligned_bounding_box_features = data


def _add_if_not_exists(shape_collection: dict[str, ShapeFeatures], path: str):
    if path in shape_collection:
        return

    shape_collection[path] = ShapeFeatures()


def _read_np_array(array_str: str) -> np.array:
    # Contains strings
    if array_str.__contains__("'"):
        arr = array_str[2:-2].split("\' \'")
        return np.array(arr)
    # Just an int array
    else:
        array_str = array_str.strip()
        arr = array_str[1:-1].strip().split()
        return np.array(arr, dtype=float)

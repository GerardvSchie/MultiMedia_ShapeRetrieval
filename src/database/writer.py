import csv
import os
import numpy as np
from src.object.shape import Shape


class DatabaseWriter:
    @staticmethod
    def write_all_shape_features(shape_list: [Shape]):
        os.makedirs('data/database/original', exist_ok=True)
        DatabaseWriter.write_other_features(shape_list, "data/database/original")
        DatabaseWriter.write_mesh_features(shape_list, "data/database/original")
        DatabaseWriter.write_convex_hull_features(shape_list, "data/database/original")
        DatabaseWriter.write_normalization_features(shape_list, "data/database/original")

    @staticmethod
    def write_other_features(shape_list: [Shape], database_dir):
        database_path = os.path.join(database_dir, "other.csv")

        with open(database_path, "w", newline='') as f:
            writer = csv.writer(f)

            # Write header to file
            header = [
                "path", "class", "aabb_p0", "aabb_p1",
            ]
            writer.writerow(header)
            for shape in shape_list:
                writer.writerow(DatabaseWriter.other_features_to_list(shape))

    @staticmethod
    def write_mesh_features(shape_list: [Shape], database_dir):
        database_path = os.path.join(database_dir, "mesh.csv")

        with open(database_path, "w", newline='') as f:
            writer = csv.writer(f)

            # Write header to file
            header = [
                "path",
                "nr_of_vertices", "nr_of_faces",
                "surface_area", "volume",
            ]
            writer.writerow(header)
            for shape in shape_list:
                writer.writerow(DatabaseWriter.mesh_features_to_list(shape))

    @staticmethod
    def write_convex_hull_features(shape_list: [Shape], database_dir):
        database_path = os.path.join(database_dir, "convex_hull.csv")

        with open(database_path, "w", newline='') as f:
            writer = csv.writer(f)

            # Write header to file
            header = [
                "path",
                "nr_of_vertices", "nr_of_faces",
                "surface_area", "volume",
            ]
            writer.writerow(header)
            for shape in shape_list:
                writer.writerow(DatabaseWriter.convex_hull_features_to_list(shape))

    @staticmethod
    def write_normalization_features(shape_list: [Shape], database_dir):
        database_path = os.path.join(database_dir, "normalization.csv")
        with open(database_path, "w", newline='') as f:
            writer = csv.writer(f)

            # Write header to file
            header = [
                "path",
                "distance_to_center", "scale",
                "alignment",
            ]
            writer.writerow(header)
            for shape in shape_list:
                writer.writerow(DatabaseWriter.normalization_features_to_list(shape))

    @staticmethod
    def other_features_to_list(shape: Shape) -> [object]:
        identifier: np.array = path_to_array(shape.geometries.path)
        return [
            identifier, shape.features.true_class,
            shape.features.aabb_min_bound, shape.features.aabb_max_bound,
        ]

    @staticmethod
    def mesh_features_to_list(shape: Shape) -> [object]:
        identifier: np.array = path_to_array(shape.geometries.path)
        return [
            identifier,
            shape.features.mesh_features.nr_vertices, shape.features.mesh_features.nr_faces,
            shape.features.mesh_features.surface_area, shape.features.mesh_features.volume,
        ]

    @staticmethod
    def convex_hull_features_to_list(shape: Shape) -> [object]:
        identifier: np.array = path_to_array(shape.geometries.path)
        return [
            identifier,
            shape.features.convex_hull_features.nr_vertices, shape.features.convex_hull_features.nr_faces,
            shape.features.convex_hull_features.surface_area, shape.features.convex_hull_features.volume,
        ]

    @staticmethod
    def normalization_features_to_list(shape: Shape) -> [object]:
        identifier: np.array = path_to_array(shape.geometries.path)
        return [
            identifier,
            shape.features.normalization_features.distance_to_center,
            shape.features.normalization_features.scale,
            shape.features.normalization_features.alignment,
            # TODO: Flip test
        ]


def path_to_array(path: str):
    identifier = []
    while len(path) > 0:
        path, tail = os.path.split(path)
        identifier.append(tail)

    identifier.reverse()
    return np.array(identifier)

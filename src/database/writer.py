import csv
import os
import numpy as np
from src.object.shape import Shape


class DatabaseWriter:
    DESCRIPTORS_HEADER = ["path", "surface_area", "compactness", "rectangularity", "diameter", "eccentricity", "convexity", "major_eccentricity", "minor_eccentricity"]
    FEATURES_HEADER = [
        'path', 'class', 'mesh_is_watertight', 'diameter',
        'mesh_nr_vertices', 'mesh_nr_faces', 'mesh_surface_area', 'mesh_volume',
        'convex_hull_nr_vertices', 'convex_hull_nr_faces', 'convex_hull_surface_area', 'convex_hull_volume',
        'bounding_box_p0', 'bounding_box_p1', 'bounding_box_surface_area', 'bounding_box_volume', 'bounding_box_diameter',
        'distance_to_center', 'scale', 'alignment', 'correctly_oriented_axes', 'eigenvalues',
    ]

    @staticmethod
    def write_features(shape_list: [Shape], path: str):
        os.makedirs(os.path.split(path)[0], exist_ok=True)

        with open(path, "w", newline='') as f:
            writer = csv.writer(f)

            # Write header to file
            writer.writerow(DatabaseWriter.FEATURES_HEADER)
            for shape in shape_list:
                writer.writerow(DatabaseWriter.get_features_list(shape))

    @staticmethod
    def write_descriptors(shape_list: [Shape], path: str):
        os.makedirs(os.path.split(path)[0], exist_ok=True)

        with open(path, "w", newline='') as f:
            writer = csv.writer(f)

            # Write header to file
            writer.writerow(DatabaseWriter.DESCRIPTORS_HEADER)
            for shape in shape_list:
                writer.writerow(DatabaseWriter.get_descriptors_list(shape))

    @staticmethod
    def get_features_list(shape: Shape) -> [object]:
        return [
            # Identifier
            path_to_array(shape.geometries.path),

            # General features
            shape.features.true_class,
            shape.features.is_watertight,
            shape.features.diameter,

            # Mesh features
            shape.features.mesh_features.nr_vertices,
            shape.features.mesh_features.nr_faces,
            shape.features.mesh_features.surface_area,
            shape.features.mesh_features.volume,

            # Convex hull features
            shape.features.convex_hull_features.nr_vertices,
            shape.features.convex_hull_features.nr_faces,
            shape.features.convex_hull_features.surface_area,
            shape.features.convex_hull_features.volume,

            # Axis aligned bounding box features
            shape.features.axis_aligned_bounding_box_features.min_bound,
            shape.features.axis_aligned_bounding_box_features.max_bound,
            shape.features.axis_aligned_bounding_box_features.surface_area,
            shape.features.axis_aligned_bounding_box_features.volume,
            shape.features.axis_aligned_bounding_box_features.diameter,

            # Normalization features
            shape.features.normalization_features.distance_to_center,
            shape.features.normalization_features.scale,
            shape.features.normalization_features.alignment,
            shape.features.normalization_features.flip,
            shape.features.normalization_features.eigenvalues,
        ]

    @staticmethod
    def get_descriptors_list(shape: Shape) -> [object]:
        return [
            # Identifier
            path_to_array(shape.geometries.path),

            # Global descriptors
            shape.descriptors.surface_area,
            shape.descriptors.compactness,
            shape.descriptors.rectangularity,
            shape.descriptors.diameter,
            shape.descriptors.eccentricity,

            shape.descriptors.convexity,
            shape.descriptors.minor_eccentricity,
            shape.descriptors.major_eccentricity,
        ]


def path_to_array(path: str):
    identifier = []
    while len(path) > 0:
        path, tail = os.path.split(path)
        identifier.append(tail)

    identifier.reverse()
    return np.array(identifier)

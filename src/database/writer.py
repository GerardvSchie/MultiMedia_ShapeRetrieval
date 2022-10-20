import csv
import os
import numpy as np
from src.object.shape import Shape


class DatabaseWriter:
    @staticmethod
    def write_features(shape_list: [Shape], path: str):
        os.makedirs('data/database', exist_ok=True)

        with open(path, "w", newline='') as f:
            writer = csv.writer(f)

            # Write header to file
            header = [
                'path', 'class', 'mesh_is_watertight', 'diameter', 'mesh_nr_vertices', 'mesh_nr_faces',
                'mesh_surface_area', 'mesh_volume', 'ch_nr_vertices', 'ch_nr_faces', 'ch_surface_area', 'ch_volume',
                'bb_p0', 'bb_p1', 'bb_surface_area', 'bb_volume', 'bb_diameter', 'distance_to_center', 'scale',
                'alignment', 'correctly_oriented_axes', 'eigenvalue_s1', 'eigenvalue_s2', 'eigenvalue_s3',
            ]
            writer.writerow(header)
            for shape in shape_list:
                writer.writerow([
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
                    shape.features.normalization_features.eigenvalue_s1,
                    shape.features.normalization_features.eigenvalue_s2,
                    shape.features.normalization_features.eigenvalue_s3,
                ])

    @staticmethod
    def write_descriptors(shape_list: [Shape], path: str):
        os.makedirs('data/database', exist_ok=True)

        with open(path, "w", newline='') as f:
            writer = csv.writer(f)

            # Write header to file
            header = [
                "path", "surface_area", "compactness", "rectangularity", "diameter", "eccentricity",
            ]
            writer.writerow(header)
            for shape in shape_list:
                writer.writerow([
                    # Identifier
                    path_to_array(shape.geometries.path),

                    # Global descriptors
                    shape.descriptors.surface_area,
                    shape.descriptors.compactness,
                    shape.descriptors.rectangularity,
                    shape.descriptors.diameter,
                    shape.descriptors.eccentricity,
                ])


def path_to_array(path: str):
    identifier = []
    while len(path) > 0:
        path, tail = os.path.split(path)
        identifier.append(tail)

    identifier.reverse()
    return np.array(identifier)

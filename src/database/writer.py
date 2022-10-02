import csv
from src.object.shape import Shape


def write_to_file(shape_list: [Shape]):
    with open("data/database.csv", "w", newline='') as f:
        writer = csv.writer(f)

        # Write row to file
        header = [
            "path", "class",
            "mesh_nr_of_vertices", "mesh_nr_of_faces",
            "mesh_surface_area", "mesh_volume",
            "convex_hull_nr_of_vertices", "convex_hull_nr_of_faces",
            "convex_hull_surface_area", "convex_hull_volume",
        ]
        writer.writerow(header)

        # Write the data to the file
        for shape in shape_list:
            data = [
                shape.geometries.path, shape.features.true_class,
                shape.features.mesh_features.nr_vertices, shape.features.mesh_features.nr_faces,
                shape.features.mesh_features.surface_area, shape.features.mesh_features.volume,
                shape.features.convex_hull_features.nr_vertices, shape.features.convex_hull_features.nr_faces,
                shape.features.convex_hull_features.surface_area, shape.features.convex_hull_features.volume,
            ]
            writer.writerow(data)

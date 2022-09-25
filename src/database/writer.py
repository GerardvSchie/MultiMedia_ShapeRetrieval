import csv
from src.object.shape import Shape


def write_to_file(shape_list: [Shape]):
    with open("data/database.csv", "w", newline='') as f:
        writer = csv.writer(f)

        # Write row to file
        header = [
            "path", "class",
            "nr_of_vertices", "nr_of_faces",
            "mesh_area", "convex_hull_area", "bounding_box_area",
        ]
        writer.writerow(header)

        # Write the data to the file
        for shape in shape_list:
            data = [
                shape.geometries.path, shape.features.true_class,
                shape.features.nr_vertices, shape.features.nr_faces,
                shape.features.mesh_area, shape.features.convex_hull_area, shape.features.bounding_box_area,
            ]
            writer.writerow(data)

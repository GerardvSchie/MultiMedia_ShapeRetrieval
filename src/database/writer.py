import csv
from src.object.shape import Shape


def write_to_file(shape_list: [Shape]):
    with open("data/database.csv", "w", newline='') as f:
        writer = csv.writer(f)

        # Write row to file
        header = ["path", "class", "nr_of_vertices", "nr_of_faces", "bounding_box"]
        writer.writerow(header)

        # Write the data to the file
        for shape in shape_list:
            data = [shape.path, shape.features.true_class, shape.features.nr_vertices, shape.features.nr_faces, shape.features.axis_aligned_bounding_box]
            writer.writerow(data)

import csv
import os.path

from src.object.features import Features

dataPaths = list()


def read_from_file() -> dict[str, Features]:
    database_path = "data/database.csv"

    # Features file does not exist
    if not os.path.exists(database_path):
        return {}

    # File exists, load all features
    with open("data/database.csv", "r") as f:
        feature_dict = {}
        reader = csv.reader(f)
        # Skip header
        next(reader)

        # Read the lines from the file
        for features in reader:
            data = Features()
            data.path, data.true_class, data.nr_vertices, data.nr_faces, data.mesh_area, data.convex_hull_area, data.bounding_box_area = features

            # Cast to types
            data.nr_vertices = int(data.nr_vertices)
            data.nr_faces = int(data.nr_faces)
            data.mesh_area = float(data.mesh_area)
            data.convex_hull_area = float(data.convex_hull_area)
            data.bounding_box_area = float(data.bounding_box_area)

            # Add to dict
            feature_dict[data.path] = data

            dataPaths.append(data.path)

        return feature_dict

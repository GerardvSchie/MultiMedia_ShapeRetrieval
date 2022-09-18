import csv
import os.path

from src.object.features import Features


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
            data.path, data.true_class, data.nr_vertices, data.nr_faces, data.axis_aligned_bounding_box = features

            # Cast to types
            data.nr_vertices = int(data.nr_vertices)
            data.nr_faces = int(data.nr_faces)

            # Add to dict
            feature_dict[data.path] = data

        return feature_dict

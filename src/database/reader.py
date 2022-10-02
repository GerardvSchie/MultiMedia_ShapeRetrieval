import csv
import os.path

from src.object.features.shape_features import ShapeFeatures

dataPaths = list()


def read_from_file() -> dict[str, ShapeFeatures]:
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
            data: ShapeFeatures = ShapeFeatures()

            data.path, data.true_class, \
                data.mesh_features.nr_vertices, data.mesh_features.nr_faces, \
                data.mesh_features.surface_area, data.mesh_features.volume, \
                data.convex_hull_features.nr_vertices, data.convex_hull_features.nr_faces, \
                data.convex_hull_features.surface_area, data.convex_hull_features.volume = features

            # Cast to types
            data.mesh_features.nr_vertices = int(data.mesh_features.nr_vertices)
            data.mesh_features.nr_faces = int(data.mesh_features.nr_faces)
            data.mesh_features.surface_area = float(data.mesh_features.surface_area)
            data.mesh_features.volume = float(data.mesh_features.volume)

            data.convex_hull_features.nr_vertices = int(data.convex_hull_features.nr_vertices)
            data.convex_hull_features.nr_faces = int(data.convex_hull_features.nr_faces)
            data.convex_hull_features.surface_area = float(data.convex_hull_features.surface_area)
            data.convex_hull_features.volume = float(data.convex_hull_features.volume)

            # Add to dict
            feature_dict[data.path] = data

            dataPaths.append(data.path)

        return feature_dict

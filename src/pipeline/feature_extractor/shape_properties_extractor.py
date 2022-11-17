import numpy as np

from src.controller.geometries_controller import GeometriesController
from src.object.shape import Shape
from src.object.properties import Properties


class ShapePropertyExtractor:
    @staticmethod
    def shape_propertizer(shape: Shape) -> bool:
        if not shape.properties.missing_values():
            return False

        # Fixed seed
        np.random.seed(0)

        GeometriesController.calculate_mesh(shape.geometries)
        vn = np.asarray(shape.geometries.mesh.sample_points_uniformly(number_of_points=5000, seed=0).points)

        # D1
        indices = np.random.choice(len(vn), 5000, replace=False)
        d1 = ShapePropertyExtractor.calc_d1(vn[indices])
        shape.properties.d1 = ShapePropertyExtractor.create_and_normalize_hist(d1, Properties.MAX['d1'])

        # D2
        indices = np.random.choice(len(vn), 4000, replace=False)
        indices_meshgrid = np.meshgrid(indices[:2000], indices[2000:])
        indices_meshgrid = np.array(indices_meshgrid).T.reshape(-1, 2)
        d2 = ShapePropertyExtractor.calc_d2(vn[indices_meshgrid[:, 0]], vn[indices_meshgrid[:, 1]])
        shape.properties.d2 = ShapePropertyExtractor.create_and_normalize_hist(d2, Properties.MAX['d2'])

        # D3
        indices = np.random.choice(len(vn), 600, replace=False)
        arr = np.meshgrid(indices[:200], indices[200:400], indices[400:])
        indices_meshgrid = np.array(arr).T.reshape(-1, 3)
        d3 = ShapePropertyExtractor.calc_d3(vn[indices_meshgrid[:, 0]], vn[indices_meshgrid[:, 1]], vn[indices_meshgrid[:, 2]])
        shape.properties.d3 = ShapePropertyExtractor.create_and_normalize_hist(d3, Properties.MAX['d3'])

        # A3
        a3 = ShapePropertyExtractor.calc_a3(vn[indices_meshgrid[:, 0]], vn[indices_meshgrid[:, 1]], vn[indices_meshgrid[:, 2]])
        shape.properties.a3 = ShapePropertyExtractor.create_and_normalize_hist(a3, Properties.MAX['a3'])

        # D4 source range: https://math.stackexchange.com/questions/975968/the-maximum-volume-of-tetrahedron
        indices = np.random.choice(len(vn), 200, replace=False)
        abcd_indices = np.meshgrid(indices[:50], indices[50:100], indices[100:150], indices[150:])
        abcd_indices_meshgrid = np.array(abcd_indices).T.reshape(-1, 4)
        d4 = ShapePropertyExtractor.calc_d4(vn[abcd_indices_meshgrid[:, 0]], vn[abcd_indices_meshgrid[:, 1]], vn[abcd_indices_meshgrid[:, 2]], vn[abcd_indices_meshgrid[:, 3]])
        shape.properties.d4 = ShapePropertyExtractor.create_and_normalize_hist(d4, Properties.MAX['d4'])

        return True

    @staticmethod
    def calc_a3(v1, v2, v3):
        v12 = v1 - v2
        v32 = v3 - v2
        dot = np.sum(np.multiply(v12, v32), axis=1)
        cosine_angle = dot / (np.linalg.norm(v12, axis=1) * np.linalg.norm(v32, axis=1))
        rad_angle = np.arccos(cosine_angle)
        return rad_angle

    @staticmethod
    def calc_d1(vertices):
        return np.linalg.norm(vertices, axis=1)

    @staticmethod
    def calc_d2(vertices_1, vertices_2):
        edges = vertices_2 - vertices_1
        return np.linalg.norm(edges, axis=1)

    @staticmethod
    def calc_d3(v1, v2, v3):
        v21 = v2 - v1
        v31 = v3 - v1
        return np.sqrt(np.linalg.norm(np.cross(v21, v31, axis=1), axis=1) / 2)

    @staticmethod
    def calc_d4(v1, v2, v3, v4):
        v14 = v1 - v4
        v24 = v2 - v4
        v34 = v3 - v4
        dot = np.sum(np.multiply(v14, np.cross(v24, v34)), axis=1)
        return np.cbrt(np.abs(dot) / 6)

    @staticmethod
    def create_and_normalize_hist(data: [float], max_value: float):
        hist, bin_edges = np.histogram(data, bins=Properties.NR_BINS, range=(0, max_value))
        hist = hist / np.sum(hist)  # Normalize
        return hist
